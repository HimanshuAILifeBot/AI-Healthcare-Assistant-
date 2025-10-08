#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║    Healthcare Voice Agent - Neon DB Setup Script      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}❌ Error: requirements.txt not found${NC}"
    echo -e "${YELLOW}   Please run this script from the backend directory${NC}"
    exit 1
fi

# Step 1: Check Python
echo -e "${BLUE}📋 Step 1: Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✅ ${PYTHON_VERSION} found${NC}"
echo ""

# Step 2: Create virtual environment if it doesn't exist
echo -e "${BLUE}📋 Step 2: Setting up virtual environment...${NC}"
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}   Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi
echo ""

# Step 3: Activate virtual environment
echo -e "${BLUE}📋 Step 3: Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✅ Virtual environment activated${NC}"
echo ""

# Step 4: Install dependencies
echo -e "${BLUE}📋 Step 4: Installing dependencies...${NC}"
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt
echo -e "${GREEN}✅ Dependencies installed${NC}"
echo ""

# Step 5: Check .env file
echo -e "${BLUE}📋 Step 5: Checking environment configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  .env file not found${NC}"
    echo -e "${YELLOW}   Creating .env from .env.example...${NC}"
    cp .env.example .env
    echo ""
    echo -e "${RED}╔════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║              IMPORTANT: ACTION REQUIRED!               ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}📝 Please update the .env file with your Neon DB credentials:${NC}"
    echo ""
    echo -e "   1. Go to ${BLUE}https://neon.tech${NC}"
    echo -e "   2. Create a new project (or use existing)"
    echo -e "   3. Copy the connection string"
    echo -e "   4. Open ${YELLOW}backend/.env${NC}"
    echo -e "   5. Replace NEON_DATABASE_URL with your connection string"
    echo ""
    echo -e "${YELLOW}Example:${NC}"
    echo -e "   NEON_DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/dbname?sslmode=require"
    echo ""
    echo -e "${YELLOW}After updating .env, run this script again.${NC}"
    exit 1
else
    echo -e "${GREEN}✅ .env file exists${NC}"
fi
echo ""

# Step 6: Test database connection
echo -e "${BLUE}📋 Step 6: Testing database connection...${NC}"
python3 test_neon_connection.py
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Database connection test failed${NC}"
    echo -e "${YELLOW}   Please check your NEON_DATABASE_URL in .env file${NC}"
    exit 1
fi
echo ""

# Step 7: Initialize database schema
echo -e "${BLUE}📋 Step 7: Would you like to initialize the database schema?${NC}"
echo -e "${YELLOW}   This will create all necessary tables in your Neon DB.${NC}"
read -p "   Initialize now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 init_neon_schema.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Database schema initialized successfully${NC}"
    else
        echo -e "${RED}❌ Schema initialization failed${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⏭️  Skipping schema initialization${NC}"
    echo -e "${YELLOW}   Run manually with: python3 init_neon_schema.py${NC}"
fi
echo ""

# Final summary
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║            🎉 Setup Complete Successfully! 🎉           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📚 Next steps:${NC}"
echo ""
echo -e "   1. Start the backend server:"
echo -e "      ${YELLOW}uvicorn main:app --reload${NC}"
echo ""
echo -e "   2. The API will be available at:"
echo -e "      ${BLUE}http://localhost:8000${NC}"
echo ""
echo -e "   3. API Documentation:"
echo -e "      ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo -e "${GREEN}✨ Your Healthcare Voice Agent is ready to go!${NC}"
echo ""
