export const loginData = {
  loginUrl: 'https://practicetestautomation.com/practice-test-login/',
  validUsername: 'student',
  validPassword: 'Password123',
  invalidUsername: 'incorrectUser',
  invalidPassword: 'incorrectPassword',
  loggedInUrlPart: '/logged-in-successfully/',
  logoutButtonSelector: "xpath=//a[text()='Log out' or text()='Log Out']",
  successMessageLocator: "xpath=//h1[contains(., 'Logged In Successfully')] | //p[contains(., 'Logged In Successfully')]",
  errorMessages: {
    invalidUsername: 'Your username is invalid!',
    invalidPassword: 'Your password is invalid!',
  },
};
