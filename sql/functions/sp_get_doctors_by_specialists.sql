CREATE OR REPLACE FUNCTION sp_get_doctors_by_specialists(specialists TEXT[], filter_date DATE DEFAULT NULL)
RETURNS TABLE (
    doctor_id INT,
    name TEXT,
    specialization TEXT,
    rating NUMERIC,
    fees INT,
    hospital TEXT,
    next_available_date DATE,
    start_time TIME,
    end_time TIME,
    slot_id INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        d.id,
        d.name::TEXT,
        d.specialization::TEXT,
        d.rating,
        CAST(d.consultation_fee AS INT) as fees,  -- Use actual consultation fee
        h.name::TEXT,
        a.available_date,
        a.start_time,
        a.end_time,
        a.id
    FROM doctors d
    JOIN hospitals h ON d.hospital_id = h.id
    LEFT JOIN availability_slots a ON d.id = a.doctor_id
    WHERE d.specialization = ANY(specialists)
    AND (filter_date IS NULL OR a.available_date = filter_date)
    ORDER BY a.available_date, a.start_time;
END;
$$ LANGUAGE plpgsql;
