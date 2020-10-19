import * as React from 'react';
import { Socket } from './Socket';
import { GoogleLogin } from 'react-google-login';

function handleGoogleOAuthLogin(response) {
    console.log("Google auth reached.");
    
    const name = response.profileObj.name;
    const email = response.profileObj.email;
    const imageUrl = response.profileObj.imageUrl;
    
    Socket.emit('new google user', {
        'name': name,
        'email': email,
        'imageUrl': imageUrl
    });
    
    console.log(`Sent the name ${name} and email ${email} to server!`);
}

function handleOnFailure(){
    console.log("Login not successful");
}

export function GoogleButton() {
    return <GoogleLogin
                clientId={'836600659281-eeutvpmf60kb2f2jfhcju5kfnebbsuu2.apps.googleusercontent.com'}
                buttonText="Login"
                onSuccess={handleGoogleOAuthLogin}
                onFailure={handleOnFailure}
                cookiePolicy={'single_host_origin'}
                // render={renderProps => (
                // <button onClick={renderProps.onClick} disabled={renderProps.disabled}>
                //     This is my custom Google button
                // </button>)}
                />
}