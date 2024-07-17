# MacroSurferFunctions

This repository contains a list of Firestore API functions to support [MacroSurfer](https://app.macrosurfer.com). These functions facilitate interaction with the Firestore database to perform various CRUD (Create, Read, Update, Delete) operations required by the MacroSurfer application.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Functions](#functions)
  - [Create Functions](#create-functions)
  - [Read Functions](#read-functions)
  - [Update Functions](#update-functions)
  - [Delete Functions](#delete-functions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

To get started with using the Firestore API functions for MacroSurfer, clone this repository and follow the installation instructions below.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/MacroSurferFunctions.git
    cd MacroSurferFunctions
    ```

2. Install the required dependencies:
    ```bash
    npm install
    ```

3. Set up your Firebase project and Firestore database:
    - Go to the [Firebase Console](https://console.firebase.google.com/).
    - Create a new project or use an existing project.
    - Enable Firestore in your Firebase project.
    - Obtain the Firebase configuration and update your project with these details.

4. Update the Firestore configuration in the project:
    ```javascript
    // firebaseConfig.js
    export const firebaseConfig = {
        apiKey: "YOUR_API_KEY",
        authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
        projectId: "YOUR_PROJECT_ID",
        storageBucket: "YOUR_PROJECT_ID.appspot.com",
        messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
        appId: "YOUR_APP_ID",
        measurementId: "YOUR_MEASUREMENT_ID"
    };
    ```

## Functions

### Create Functions

- **createUser(userData)**: Adds a new user to the Firestore database.
    ```javascript
    async function createUser(userData) {
        const userRef = firestore.collection('users').doc();
        await userRef.set(userData);
        return userRef.id;
    }
    ```

- **createMacro(macroData)**: Adds a new macro entry to the Firestore database.
    ```javascript
    async function createMacro(macroData) {
        const macroRef = firestore.collection('macros').doc();
        await macroRef.set(macroData);
        return macroRef.id;
    }
    ```

### Read Functions

- **getUser(userId)**: Retrieves a user by their ID from the Firestore database.
    ```javascript
    async function getUser(userId) {
        const userRef = firestore.collection('users').doc(userId);
        const doc = await userRef.get();
        if (doc.exists) {
            return doc.data();
        } else {
            throw new Error('No such document!');
        }
    }
    ```

- **getMacrosByUser(userId)**: Retrieves all macros associated with a specific user.
    ```javascript
    async function getMacrosByUser(userId) {
        const macrosRef = firestore.collection('macros').where('userId', '==', userId);
        const snapshot = await macrosRef.get();
        const macros = [];
        snapshot.forEach(doc => {
            macros.push({ id: doc.id, ...doc.data() });
        });
        return macros;
    }
    ```

### Update Functions

- **updateUser(userId, userData)**: Updates user information in the Firestore database.
    ```javascript
    async function updateUser(userId, userData) {
        const userRef = firestore.collection('users').doc(userId);
        await userRef.update(userData);
    }
    ```

- **updateMacro(macroId, macroData)**: Updates a macro entry in the Firestore database.
    ```javascript
    async function updateMacro(macroId, macroData) {
        const macroRef = firestore.collection('macros').doc(macroId);
        await macroRef.update(macroData);
    }
    ```

### Delete Functions

- **deleteUser(userId)**: Deletes a user from the Firestore database.
    ```javascript
    async function deleteUser(userId) {
        const userRef = firestore.collection('users').doc(userId);
        await userRef.delete();
    }
    ```

- **deleteMacro(macroId)**: Deletes a macro entry from the Firestore database.
    ```javascript
    async function deleteMacro(macroId) {
        const macroRef = firestore.collection('macros').doc(macroId);
        await macroRef.delete();
    }
    ```

## Usage

To use these functions, import them into your project and call them with the appropriate parameters. Ensure you have initialized Firebase and Firestore in your project before invoking these functions.

```javascript
import { createUser, getUser, updateUser, deleteUser } from './path/to/functions';

// Example usage
const userId = await createUser({ name: 'John Doe', email: 'john@example.com' });
const user = await getUser(userId);
await updateUser(userId, { email: 'john.doe@example.com' });
await deleteUser(userId);