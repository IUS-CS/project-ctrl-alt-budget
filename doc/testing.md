# Testing Documentation

## Overview

This document explains the testing completed so far for the Ctrl-Alt-Budget project. Up to this point, most of the testing has been done locally while developing the application. The main focus has been on checking that important routes load correctly, authentication works, and frontend pages connect to the backend as expected.

## Testing Approach

Testing has mainly been done through manual testing. The project was run locally using Flask, and different pages and routes were checked in the browser. Some backend behavior was also checked during development by submitting forms and confirming the expected redirects, messages, and page access.

At this stage, the team has mainly been testing whether:
- pages load correctly
- routes connect to the correct templates
- account creation and login work
- protected pages require login
- logout works correctly
- backend routes respond as expected during development

## Features Tested

### Homepage and Navigation

The homepage was tested to make sure it loads correctly and that users can navigate to the main pages of the application.

**Expected result:**  
The homepage should load without errors, and links should go to the correct pages.

**Observed result:**  
The homepage loaded correctly during local testing, and navigation worked for the main pages that were available.

### Account Creation

The signup page was tested by creating a new account locally.

**Expected result:**  
A user should be able to submit the signup form, create an account, and be redirected to the dashboard.

**Observed result:**  
Account creation worked during local testing, and the user was redirected to the dashboard after signup.

### Login

The login page was tested using a created account.

**Expected result:**  
A user with valid credentials should be able to log in and access protected pages.

**Observed result:**  
Login worked during local testing with a valid account.

### Logout

The logout route was tested after logging in.

**Expected result:**  
The user session should end, and the user should no longer have access to protected pages until logging in again.

**Observed result:**  
Logout worked during testing and removed access to protected pages until the user logged in again.

### Protected Routes

Protected pages such as the dashboard were tested while logged in and while logged out.

**Expected result:**  
Logged-in users should be able to access protected pages, while logged-out users should be redirected to the login page.

**Observed result:**  
Protected route behavior worked as expected during local testing.

### Backend Route and Form Connection

Frontend forms and backend routes related to authentication were checked together to make sure the frontend and backend were connected properly.

**Expected result:**  
Submitting login and signup forms should send data to the backend and return the correct result.

**Observed result:**  
The forms and backend auth routes worked together correctly during testing.

## Tools and Methods Used

The following methods were used during testing:
- local Flask runtime testing
- manual browser testing
- checking redirects and page access
- reviewing error messages during development

## Current Limitations

There are still some testing limitations at this stage of the project:
- most testing so far has been manual instead of automated
- full database testing has not been completed in every environment
- some features still need more complete end-to-end testing
- future budgeting and reporting features will need additional testing once they are finished

## Future Testing Plans

As the project continues, testing should be expanded to include:
- more complete database testing
- form validation testing
- route testing for additional features
- more end-to-end testing between frontend and backend
- automated testing where appropriate

## Summary

So far, testing has shown that the basic authentication flow and route connections are working locally. Account creation, login, logout, and protected page access have all been checked during development. More testing will still be needed as the rest of the project is completed.