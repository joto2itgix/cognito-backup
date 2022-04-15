# cognito-backup
Cognito Export/Import Python Lambdas

Introduction
	Amazon Cognito lets you add user sign-up, sign-in, and access control to your web and mobile apps quickly and easily. Amazon Cognito scales to millions of users and supports sign-in with social identity providers, such as Apple, Facebook, Google, and Amazon, and enterprise identity providers via SAML 2.0 and OpenID Connect.  
	If you need to backup an Amazon Gognito User Pool, you will notice that there is no native solution provided by Amazon. However  Amazon User Pool has a very flexible API that we are going to use in order to backup our users.
	It’s very important to have the user profiles and associated data safe, particularly because backups are not only vital in preventing accidents (e.g. unintentionally deleting data), but are also essential in other cases such as migrating user data to a new user pool. For these reasons we decided to work on our own solution.
	Data is the new oil, then backups should typically prevent it from catching fire. But how to do it if the core service you rely on does not provide an out-of-the-box backup solution? The answer is pretty simple, develop one! And this is what we are going to in this tutorial.
	What seems to be an obvious and routine procedure can sometimes become quite tricky.  This solution is custom built, but design to match high variety of use cases. Here is a guide explaining how to develop a backup-restore solution for Amazon Cognito users.
	 This tutorial does not cover the entire architecture setup in detail, but will present the core part of the implementation we felt would be most relevant. For more information please refer to the AWS documentation.
	Will not show how associate AWS Lambda to a trigger event. In our case, we will trigger event manually.
	To accomplish our go we will use Python based Lambda functions. One for exporting Cognito users into CSV, uploads and store it into S3 bucket. One to clean the second Cognito, and one to get the CSV file and import it into the backup Cognito instance.