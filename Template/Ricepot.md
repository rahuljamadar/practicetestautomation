# Ricepot Test Plan

## Test Plan
This document describes the test plan for the Restful Booker API hosted at https://restful-booker.herokuapp.com.

## Objective
The goal of this test plan is to ensure the quality, functionality, and reliability of the Restful Booker API. The API is designed to handle booking requests for a fictional hotel booking system.

## Scope
Scope of Test Plan for Restful Booker API:

1. Functional Testing
   - Verify the correctness and functionality of all API endpoints as per the API documentation.
   - Test various scenarios for booking creation, modification, and cancellation.
   - Validate user authentication and authorization mechanisms for protected endpoints.

2. Data Validation Testing
   - Ensure that the API correctly validates input data, rejecting invalid requests.
   - Test boundary values for input fields to check for any unexpected behavior.
   - Validate the accuracy of data returned in responses.

3. Error Handling Testing
   - Verify that appropriate error codes and messages are returned for invalid requests.
   - Check error responses for sensitive information disclosure.
   - Validate the API's ability to handle unexpected errors gracefully.

4. Performance Testing
   - Assess the API's response time under normal and peak loads to identify potential bottlenecks.
   - Measure the API's throughput and scalability to handle concurrent requests.

5. Security Testing
   - Conduct security assessments to identify vulnerabilities such as SQL injection, XSS, etc.
   - Validate the API's compliance with secure data transmission practices (e.g., HTTPS).
   - Check for proper access controls to prevent unauthorized access to sensitive resources.

6. Integration Testing
   - Verify interactions between different API endpoints and services.
   - Test data consistency across related endpoints.

7. Compatibility Testing
   - Test the API on different platforms, browsers, and devices to ensure cross-compatibility.

8. Documentation Review
   - Assess the clarity, completeness, and accuracy of the API documentation.
   - Verify that the API documentation is in sync with the actual API behavior.

9. Load Testing
   - Evaluate the API's behavior under high concurrent user loads to ensure stability.

10. Regression Testing
    - Conduct regression testing after bug fixes or updates to ensure existing functionality remains intact.

11. Edge Case Testing
    - Test extreme and boundary scenarios to identify potential issues.

12. Concurrency Testing
    - Assess the API's behavior when multiple users attempt to access and modify bookings simultaneously.

13. Ad Hoc Testing
    - Perform exploratory testing to identify any hidden defects or usability issues.

14. Usability Testing
    - Evaluate the API's user-friendliness and ease of use from a developer's perspective.

15. Continuous Integration and Deployment (CI/CD) Testing
    - Validate the API's behavior within the CI/CD pipeline to ensure smooth deployments.

16. Performance Monitoring
    - Implement monitoring to track API performance in real-time.

17. Backup and Recovery Testing
    - Validate data backup and recovery procedures to ensure data integrity.

18. Internationalization Testing
    - Test the API's behavior with different language settings.

19. Rate Limiting Testing
    - Check the API's adherence to rate-limiting rules to prevent abuse.

20. Third-Party Integration Testing
    - Validate any third-party integrations for smooth functioning.

The scope of the test plan may evolve during the testing process based on feedback, changing requirements, or discoveries during testing.

## Inclusions

### Create (POST) Operations
- Test the API's ability to create new bookings using valid input data.
- Verify that appropriate error responses are returned for invalid or missing data.
- Validate that newly created bookings are stored correctly in the system.

### Read (GET) Operations
- Test the API's ability to retrieve booking information by various criteria (e.g., booking ID, date range, guest name).
- Verify that the API returns the correct data in response to read requests.
- Test for correct handling of non-existent or invalid booking IDs.

### Update (PUT) Operations
- Test the API's ability to update existing bookings with valid data.
- Verify that the API rejects invalid update requests with appropriate error responses.
- Validate that the booking data is correctly modified in the system after updates.

### Delete (DELETE) Operations
- Test the API's ability to delete bookings by providing valid booking IDs.
- Verify that the API returns appropriate responses after successful deletion.
- Validate that the deleted bookings are removed from the system.

### Boundary Testing
- Test the API with minimum and maximum allowed values for input fields.
- Validate the behavior of the API with values close to the boundaries.

### Concurrency Testing
- Test the API's behavior when multiple users try to perform CRUD operations simultaneously.
- Verify data consistency and handling of concurrent modifications.

### Data Validation
- Test the API's response to various data validation scenarios (e.g., invalid characters, data types, mandatory fields).
- Verify that the API handles validation errors appropriately.

### Authentication and Authorization
- Test CRUD operations for both authenticated and unauthenticated users.
- Verify that only authorized users can perform certain CRUD operations.

### Error Handling
- Test the API's response when invalid or malformed requests are made for CRUD operations.
- Validate that appropriate error codes and messages are returned.

### Security Testing
- Test for security vulnerabilities during CRUD operations (e.g., SQL injection, XSS).
- Verify that sensitive data is not exposed in responses.

### Performance Testing
- Evaluate the API's response time for CRUD operations under normal and peak loads.
- Measure the throughput and scalability of the API.

### Integration Testing
- Verify the interaction and data consistency between CRUD operations and other API components.

### Regression Testing
- Perform regression tests after bug fixes or updates to ensure existing CRUD functionalities remain intact.

### Documentation Review
- Assess the accuracy of API documentation related to CRUD operations.

### Load Testing
- Evaluate the API's behavior and performance during CRUD operations under high concurrent user loads.

### Compatibility Testing
- Test the API's CRUD operations on different platforms, browsers, and devices.

### Usability Testing
- Evaluate the ease of using CRUD functionalities from a developer's perspective.

### Continuous Integration and Deployment (CI/CD) Testing
- Validate the CRUD operations within the CI/CD pipeline to ensure smooth deployments.

### Rate Limiting Testing
- Check the API's adherence to rate-limiting rules for CRUD operations to prevent abuse.

### Backup and Recovery Testing
- Validate data backup and recovery procedures for CRUD-related data.

## Test Environments
- Operating systems and versions: Windows 10, macOS, Linux.
- Browsers and versions: Google Chrome, Mozilla Firefox, Microsoft Edge, Safari.
- Device types and screen sizes: desktop computers, laptops, tablets, smartphones.
- Network connectivity: Wi-Fi, cellular, wired connections.
- Hardware/software requirements: processor, memory, storage capacity needed for testing.
- Security protocols and authentication methods: passwords, tokens, certificates.
- Access permissions and roles: testers, developers, stakeholders.

### Environment Matrix
- QA: https://restful-booker.herokuapp.com/apidoc/index.html
- Pre Prod: https://restful-booker.herokuapp.com/apidoc/index.html

### Platforms
- Windows 10 – Chrome, Firefox, Edge
- macOS – Safari
- Android Mobile OS – Chrome
- iPhone Mobile OS – Safari

## Defect Reporting Procedure
- Define defect criteria: deviation from requirements, user experience issues, technical errors.
- Report defects using a designated template with detailed reproduction steps and attachments.
- Triage and prioritize defects by severity and priority.
- Track defects in a defect tracking tool or project management system.
- Assign responsibilities to testers, developers, and test leads.
- Use communication channels to update stakeholders on defect status.
- Measure defect process effectiveness with metrics like defect count, resolution time, and fix rate.

### Defect Process
- POC New Frontend: Devesh
- Backend: Sonal
- Dev Ops: Prajeeth

## Tools
- JIRA
- Mind map tool
- Snipping screenshot tool
- Word and Excel documents

## Test Strategy
- Create test scenarios and test cases for the features in scope.
- Apply the following test design techniques:
  - Equivalence Class Partitioning
  - Boundary Value Analysis
  - Decision Table Testing
  - State Transition Testing
  - Use Case Testing
- Apply expert techniques:
  - Error Guessing
  - Exploratory Testing
- Prioritize test cases.

### Testing Procedure
1. Perform smoke testing first to verify essential functionality.
2. Reject the build if smoke tests fail, and wait for a stable build before deeper testing.
3. Once a stable build passes smoke testing, execute detailed test cases.
4. Test the application on multiple supported environments simultaneously.
5. Report defects in the tracking tool and send daily status updates to dev management.

### Testing Types
- Smoke Testing and Sanity Testing
- Regression Testing and Retesting
- Usability Testing, Functionality Testing, UI Testing
- Repeat test cycles until the product meets quality standards.

### Best Practices
- Context Driven Testing: test based on application context.
- Shift Left Testing: start testing early in development.
- Exploratory Testing: use expertise to find issues beyond scripted test cases.
- End-to-End Flow Testing: validate complete user flows across multiple functionalities.

## Test Schedule
Planned test schedule for the project:
- Creating Test Plan
- Test Case Creation
- Test Case Execution
- Summary Reports Submission Date

Two sprints are planned to test the application.

## Test Deliverables
- Test Plan
- Test Scenarios
- Test Cases
- Test Reports

## Entry and Exit Criteria
### Requirement Analysis
Entry Criteria:
- Requirements documents or project details are received by the testing team.
Exit Criteria:
- Requirements are explored and understood by the testing team.
- Doubts are cleared.

### Test Execution
Entry Criteria:
- Test scenarios and test cases are signed off.
- Application is ready for testing.
Exit Criteria:
- Test case reports and defect reports are ready.

### Test Closure
Entry Criteria:
- Test case reports and defect reports are ready.
Exit Criteria:
- Test summary reports are completed.

## Risks and Mitigations
- Risk: Non-availability of a resource
  - Mitigation: Backup resource planning
- Risk: Build URL is not working
  - Mitigation: Resources will work on other tasks
- Risk: Less time for testing
  - Mitigation: Ramp up resources dynamically based on client needs

## Approvals
Team will send documents for client approval, including:
- Test Plan
- Test Scenarios
- Test Cases
- Reports

Testing will continue to the next steps only after approvals are completed.
