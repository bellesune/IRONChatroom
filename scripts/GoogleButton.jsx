import * as React from 'react';
import { Socket } from './Socket';
import { GoogleLogin } from 'react-google-login';

function handleGoogleOAuthLogin(response) {
    console.log("Google auth reached.");
 
    let name = response.profileObj.name;
    let email = response.profileObj.email;
    
    Socket.emit('new google user', {
        'name': name,
        'email': email,
    });
    
    console.log(`Sent the name ${name} and email ${email} to server!`);
}

function handleOnFailure(){
    console.log("Login not successful");
}

export function GoogleButton() {
    return <GoogleLogin
                clientId={'836600659281-eeutvpmf60kb2f2jfhcju5kfnebbsuu2.apps.googleusercontent.com'}
                buttonText="Login with Google"
                onSuccess={handleGoogleOAuthLogin}
                onFailure={handleOnFailure}
                cookiePolicy={'single_host_origin'}
            />
}