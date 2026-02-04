# Requirements Document

## Introduction

The Sahayak Automation API is a FastAPI-based web automation service that analyzes user natural language commands along with screenshots to determine and execute web automation actions. The system serves as an intelligent intermediary between human intent and web automation, translating natural language instructions into precise automation actions.

## Glossary

- **System**: The Sahayak Automation API service
- **User_Command**: Natural language instruction provided by the user
- **Screenshot**: Base64-encoded image of the current web page state
- **Automation_Action**: A specific web interaction (type, click, scroll, wait)
- **CSS_Selector**: A string pattern used to identify HTML elements
- **Action_History**: Chronological record of all automation actions performed
- **Pattern_Matcher**: Current rule-based command analysis engine
- **Vision_AI**: Future AI-powered image and command analysis system
- **Confidence_Score**: Numerical value (0.0-1.0) indicating action certainty

## Requirements

### Requirement 1: Command Analysis and Action Generation

**User Story:** As a web automation user, I want to provide natural language commands with screenshots, so that the system can determine the appropriate automation actions to perform.

#### Acceptance Criteria

1. WHEN a user submits a command with a screenshot, THE System SHALL analyze both inputs and return a specific automation action
2. WHEN the command contains "naam" or "name", THE System SHALL generate a text input action for name fields with appropriate CSS selectors
3. WHEN the command contains "email" or "e-mail", THE System SHALL generate a text input action for email fields with type='email' selectors
4. WHEN the command contains "phone" or "mobile", THE System SHALL generate a text input action for phone fields with telephone-specific selectors
5. WHEN the command contains submit keywords ("next", "submit", "continue", "proceed"), THE System SHALL generate a click action for submit buttons
6. WHEN the command contains "click", THE System SHALL generate a click action with element-specific selectors
7. WHEN the command contains "scroll", THE System SHALL generate a scroll action with directional value (up/down)
8. WHEN the command contains "wait", THE System SHALL generate a wait action with specified or default duration
9. WHEN the command contains "with [value]", THE System SHALL extract the custom value for input actions
10. WHEN no pattern matches the command, THE System SHALL return a "none" action with appropriate explanation

### Requirement 2: Action History Management

**User Story:** As a web automation user, I want to track my automation history, so that I can review past actions and monitor system usage.

#### Acceptance Criteria

1. WHEN an automation action is generated, THE System SHALL store the complete action record in history
2. WHEN storing action records, THE System SHALL include user command, URL, response details, and timestamp
3. WHEN the history exceeds 100 records, THE System SHALL remove the oldest record to maintain the limit
4. WHEN a user requests history, THE System SHALL return records in reverse chronological order (most recent first)
5. WHEN a user specifies a limit parameter, THE System SHALL return only that number of recent records
6. WHEN a user requests history clearing, THE System SHALL remove all stored action records
7. WHEN history is cleared, THE System SHALL return a success confirmation message

### Requirement 3: CSS Selector Validation

**User Story:** As a web automation developer, I want to validate CSS selector syntax, so that I can ensure automation actions will target elements correctly.

#### Acceptance Criteria

1. WHEN a CSS selector is submitted for validation, THE System SHALL check for basic syntax correctness
2. WHEN the selector has mismatched brackets, THE System SHALL return validation failure with specific error
3. WHEN the selector has mismatched parentheses, THE System SHALL return validation failure with specific error
4. WHEN the selector is empty, THE System SHALL return validation failure with appropriate error message
5. WHEN the selector is syntactically valid, THE System SHALL return validation success with the selector
6. WHEN validation encounters an exception, THE System SHALL return failure with the exception details

### Requirement 4: Usage Statistics and Analytics

**User Story:** As a system administrator, I want to monitor API usage statistics, so that I can understand system performance and user behavior patterns.

#### Acceptance Criteria

1. WHEN statistics are requested, THE System SHALL calculate total number of actions performed
2. WHEN calculating statistics, THE System SHALL provide breakdown of action types with counts
3. WHEN determining success rate, THE System SHALL calculate percentage of non-"none" actions
4. WHEN identifying patterns, THE System SHALL determine the most frequently used command
5. WHEN no history exists, THE System SHALL return zero values for all statistics
6. WHEN action history is available, THE System SHALL compute real-time statistics from current data

### Requirement 5: System Health and Service Information

**User Story:** As a system administrator, I want to monitor system health and access service information, so that I can ensure proper system operation.

#### Acceptance Criteria

1. WHEN a health check is requested, THE System SHALL return current system status and timestamp
2. WHEN providing health information, THE System SHALL include service name, version, and action history count
3. WHEN the root endpoint is accessed, THE System SHALL return comprehensive API information
4. WHEN listing endpoints, THE System SHALL provide description and usage for each available endpoint
5. WHEN service information is requested, THE System SHALL include documentation link reference

### Requirement 6: HTTP API Interface and Error Handling

**User Story:** As a client application, I want to interact with the system through well-defined HTTP endpoints, so that I can integrate automation capabilities reliably.

#### Acceptance Criteria

1. WHEN the system starts, THE System SHALL expose all endpoints on port 8000 with CORS middleware enabled
2. WHEN HTTP exceptions occur, THE System SHALL return structured error responses with status codes
3. WHEN general exceptions occur, THE System SHALL return internal server error with safe error details
4. WHEN POST requests are made to /analyze, THE System SHALL accept AnalyzeRequest model and return ActionResponse
5. WHEN GET requests are made to /history, THE System SHALL accept optional limit parameter and return HistoryResponse
6. WHEN DELETE requests are made to /history, THE System SHALL clear history and return success confirmation
7. WHEN POST requests are made to /validate, THE System SHALL accept selector string and return validation result
8. WHEN GET requests are made to /stats, THE System SHALL return current usage statistics
9. WHEN GET requests are made to /health, THE System SHALL return detailed health information

### Requirement 7: Data Models and Validation

**User Story:** As a system integrator, I want consistent data structures for all API interactions, so that I can reliably process requests and responses.

#### Acceptance Criteria

1. WHEN receiving analyze requests, THE System SHALL validate AnalyzeRequest with user_command, screenshot, and optional URL
2. WHEN returning action responses, THE System SHALL provide ActionResponse with action, selector, value, confidence, timestamp, and explanation
3. WHEN returning history data, THE System SHALL provide HistoryResponse with total count and actions list
4. WHEN screenshot data is provided, THE System SHALL accept base64-encoded image format
5. WHEN confidence scores are calculated, THE System SHALL return values between 0.0 and 1.0
6. WHEN timestamps are generated, THE System SHALL use ISO format for consistency
7. WHEN optional fields are omitted, THE System SHALL handle requests gracefully with default values

### Requirement 8: Future Vision AI Integration

**User Story:** As a product owner, I want the system designed for Vision AI integration, so that automation accuracy can be improved beyond pattern matching.

#### Acceptance Criteria

1. WHEN the current pattern matching system is replaced, THE System SHALL maintain the same API interface
2. WHEN Vision AI is integrated, THE System SHALL analyze screenshots using computer vision capabilities
3. WHEN Vision AI processes commands, THE System SHALL combine visual analysis with natural language understanding
4. WHEN confidence scores are calculated with Vision AI, THE System SHALL provide more accurate assessments
5. WHEN Vision AI generates selectors, THE System SHALL create more precise element targeting
6. WHEN the system transitions to Vision AI, THE System SHALL maintain backward compatibility with existing clients

### Requirement 9: Performance and Scalability

**User Story:** As a system administrator, I want the system to handle concurrent requests efficiently, so that multiple users can access automation services simultaneously.

#### Acceptance Criteria

1. WHEN multiple requests are received concurrently, THE System SHALL process them without blocking
2. WHEN memory usage grows, THE System SHALL maintain history limits to prevent memory exhaustion
3. WHEN response times are measured, THE System SHALL return automation actions within 2 seconds for pattern matching
4. WHEN the system is under load, THE System SHALL maintain API responsiveness for health checks
5. WHEN action history grows large, THE System SHALL implement efficient data access patterns

### Requirement 10: Security and Data Protection

**User Story:** As a security administrator, I want the system to handle sensitive data securely, so that user information and screenshots are protected.

#### Acceptance Criteria

1. WHEN screenshots are processed, THE System SHALL handle base64 data securely without persistent storage
2. WHEN CORS is configured, THE System SHALL restrict origins appropriately for production environments
3. WHEN error messages are returned, THE System SHALL avoid exposing sensitive system information
4. WHEN user commands contain personal data, THE System SHALL process them without logging sensitive details
5. WHEN action history is stored, THE System SHALL implement appropriate data retention policies