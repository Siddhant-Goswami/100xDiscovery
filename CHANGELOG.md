# Changelog

## [2.2.1] - 2024-01-11

### Fixed
- Fixed local development environment configuration
- Added fallback mechanism for environment variables
- Improved error handling for missing secrets
- Added local secrets.toml template

## [2.2.0] - 2024-01-11

### Added
- Optional Groq API key input in UI
- Fallback to keyword search when Groq key not provided
- Better error messages for API connectivity
- URL debugging information in development mode

### Changed
- Made Groq integration optional and user-configurable
- Improved API endpoint handling with proper /api prefix
- Enhanced error handling with detailed messages
- Updated search UI with configuration expander

### Fixed
- Fixed 404 errors in production by correcting API URL construction
- Fixed environment variable handling in Streamlit Cloud
- Fixed search functionality to work with/without Groq
- Improved error messages for better debugging

## [2.1.0] - 2024-01-11

### Changed
- Updated frontend environment configuration
- Added separate production and development API URLs
- Improved API client error handling
- Enhanced development debugging information

### Added
- Environment-based API URL selection
- Better error messages for API connectivity
- Development mode indicators in UI

## [2.0.0] - 2024-01-11

### Changed
- Restructured project into a monorepo with separate backend and frontend
- Removed Hugging Face Spaces integration for more flexible deployment
- Simplified environment configuration
- Made codebase more beginner-friendly

### Backend Changes
- Moved FastAPI application to `backend/` directory
- Separated backend dependencies
- Simplified API endpoint structure
- Improved error handling and validation
- Added better documentation

### Frontend Changes
- Moved Streamlit application to `frontend/src/`
- Separated frontend dependencies
- Improved API client configuration
- Enhanced error handling and user feedback
- Made UI more intuitive

## [1.0.0] - 2024-01-10

### Added
- Initial release with basic functionality
- FastAPI backend with profile management
- Streamlit frontend for user interface
- Groq integration for semantic search
- Basic CRUD operations for profiles
- Natural language search functionality
- JSON-based data storage
- Environment configuration
- Basic documentation 