# qaforge

This is one important engineering step

Before Moving ahead with coding and scripting, lets product V1 technical specification

# 1. What exactly does QAForge do - Product Definition?

QAForge is a centralized Test Management & Automation platform for managing software testing activities, test execution, reporting, and automated test execution. This project will help not just QAs or SDET but also other members like Developers, Managers and Devops people that want to monitor the projects from Testing perspective. 
The idea is similar to a simplified cobination of:
- Test Management
- Test Case Management
- Test Execution
- Test Reporting
- Defect Tracking
- Automation execution integration

This will be single where entire organizations testing projects can be integrated and used for tracking and performing QA operations. Instead of managing different test resources in differnt sources and platforms, we can use this platform for managing all our test resources.

Build a centralized platform for managing software testing activities and integrating automated test execution.

Primary Users:

| Role            | Primary responsibility                             |
| --------------- | -------------------------------------------------- |
| **Admin**       | Platform/user administration                       |
| **QA Engineer** | Test management and execution                      |
| **Developer**   | Test execution, reporting and defect collaboration |
| **Viewer**      | Read-only visibility                               |

#### V1 Scope: 

User
Project
TestSuite
TestCase
TestRun
Tag


# 2. What are the functional requirements?
The Functional Requirements for this project are mostly based on the user base, who are going to use this application.
For our first vision we will have 4 roles:
- ADMIN, QA ENGINER, DEVELOPER, VIEWER
- Each of this role will have an access to set of functionalities based on their permissions. 
- In high level view:
- Users will be able to create their own projects
- Users will be able to import their test cases in the project
- Users will be able to execute their test cases
- Users will be able to view the execution report after test execution
- Users wlll be able to Integrate Automation scripts with their test cases
- Users can add, update, delete their test cases, projects, test suites based on the roles (RBAC)
- Users will able log defects and track them. They can do operations which are related to Defect life cycle such as opening, retesting, closing defects
- Users can also view projects, test cases, reports, test suites

# 3. What are the non-functional requirements?

For Non-Functional Requirements lets define this as a learning project with production-style architecture.
V1 could target:
- Users: 50-100
- Projects: 10-50
- Test cases: 1000-10000
- Test runs: Thousands/month
- Test results: Thousands/month
- Concurrent users: ~10-50

There are initials assumptions, not facts

QA-Forge V1 is intended for a small-medium organization.

# 4. What are the actors and permissions?

Who interacts with the system ?
Admin:
- Manage Users
- Manage Projects
- Manage Automation Integrations

### QA Engineer
- Can Create Project
- Can upload Test Cases
- Can execute Test Cases
- Can View the report
- Can Run Automated Tests
- Can log Defects (Handle Defect lifecycle Processes)
- Can delete test cases, test suites

### Developer
- Can run Automated Tests
- Can view the test reports
- Can view defects (Comment on defects)

### Viewer
- Can view the Test Reports
- Can view the test cases
- Can view the defects

# 5. What entities exist?

What things exists in the system ?

This project has multiple entities which interact with each other and run the processes

- User: Represents people using QAForge
- Project: A Software Project being tested. Ex: Fennec Claims, QAForge, Payment Service
- Test Suite: A logical grouping of test cases. Authentication, Claims Processing, Regression
- Test Cases: An individual Test Scenario
- Tag: Used to categorize test cases
- Test Run: A Particular execution session
- Test Results: The result of test cases within a Test Run

In V1 we will keep the above entities itself, then we will handle other entites in later phases
- Defects
- Environments
- AutomationRun

# 6. What are their relationships?

How do we represent the fact that a particular project belongs to a particular user ?
Relationships are generally represented using using Foreign Keys

The three major relationship types:
- One-to-One
- One-to-Many
- Many-to-Many

So for our project there are multiple relationships we can build.
- User -> N:N -> Project –––> A user can manage multiple projects, but mulitple users can also belong to multiple projects
- Project -> 1:N -> Test Suite –––> A Project can have multiple Test Suites
- Test Suite -> 1:N -> Test Cases –––> A Test Suite can have multiple Test Cases
- Test Cases -> N:N -> Test Runs –––> A Test Case can have multiple Test Runs and Test Run can have multiple Test Cases
- Test Cases -> N:N -> Tags –––> A Test Case can have multiple tags, and tags can have multiple test cases
- Test Cases -> 1:N -> Test Result –––> A Test Case can have multiple Test Results 
- Test Run -> 1:N -> Test Result –––> This needs more analysis, as each Test Run can have only one Test Result. But Test Result can contain multiple Test Runs for Test Cases. 

                         ┌──────────────┐
                         │     User     │
                         └──────┬───────┘
                                │
                               1:N
                                │
                                ▼
                         ┌──────────────┐
                         │   Project    │
                         └──────┬───────┘
                                │
                  ┌─────────────┼─────────────┐
                  │             │             │
                 1:N           1:N           1:N
                  │             │             │
                  ▼             ▼             ▼
            ┌──────────┐  ┌───────────┐  ┌──────────┐
            │TestSuite │  │ TestCase  │  │  Defect  │
            └────┬─────┘  └─────┬─────┘  └────┬─────┘
                 │              │             │
                1:N             │             │
                 │              │             │
                 ▼              │             │
            ┌──────────┐        │             │
            │ TestCase │◄───────┘             │
            └────┬─────┘                      │
                 │                             │
                1:N                            │
                 │                             │
                 ▼                             │
            ┌───────────┐                      │
            │TestResult │──────────────────────┘
            └─────┬─────┘
                  │
                 N:1
                  │
                  ▼
             ┌──────────┐
             │ TestRun  │
             └──────────┘

            TestCase N:N Tag

# 7. What are the important workflows?

Workflows is a sequence of business operations that together accomplish one business goal. 
Fow now we will create a sample workflows to get started. As we move ahead in project we will get together another workflows as well

#### Workflow 1: A user wants to create a project
#### Workflow 2: A user wants to create a Test Suite
#### Workflow 3: A user wants to upload the Test Cases in Test Suite
#### Workflow 4: A user wants to log a Defect and link that defect with the test case
#### Workflow 5: A user wants to execute the Test Case generate a Report 

# 8. What are the business rules?

A set of business rules are not defined as of now
# 9. What APIs do we need?


# 10. What database structure do we need?
What data must exist, what rules must the database enfore, and why ?

- USER: We'er going to user custom django fields
- PROJECT
- PROJECT MEMBERSHIP: this is the bridge between users and projects
- TESTSUITE
- TESTCASES
- TESTCASE IDENTIFIER
- TESTCASE STATUS: DRAFT, ACTIVE, DEPRECATED
- TESTCASE PRIORITY: LOW, MEDIUM, HIGH, CRITICAL
- TAGS
- TESTRUN
- TESTRUN STATUS: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
- TESTRESULT: PASSED, FAILED, SKIPPED, BLOCKED
- DEFECT
- DEFECTSTATUS: OPEN, IN_PROGRESS, RESOLVED, REOPENED, CLOSED
- DEFECT SEVERITY: LOW, MEDIUM, HIGH, CRITICAL
- DEFECT PRIORITY: LOW, MEDIUM, HIGH, CRITICAL

Our Implementation steps, as this project would be for learning purpose as well

                        Step 1
                        ↓
                        Create repository/project directory

                        Step 2
                        ↓
                        Create Python virtual environment

                        Step 3
                        ↓
                        Install Django + DRF

                        Step 4
                        ↓
                        Create Django project

                        Step 5
                        ↓
                        Create applications

                        Step 6
                        ↓
                        Configure settings

                        Step 7
                        ↓
                        Create custom User model

                        Step 8
                        ↓
                        Create Project models

                        Step 9
                        ↓
                        Create Testing models

                        Step 10
                        ↓
                        Create Defect model

                        Step 11
                        ↓
                        Run migrations

                        Step 12
                        ↓
                        Verify database

                        Step 13
                         ↓
                        Create first API

