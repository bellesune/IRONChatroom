import * as React from 'react';
import { GoogleLogin } from 'react-google-login';
import { Socket } from './Socket';

function handleGoogleOAuthLogin(response) {
  const { name } = response.profileObj;
  const { email } = response.profileObj;
  const { imageUrl } = response.profileObj;

  Socket.emit('new google user', {
    name,
    email,
    imageUrl,
    successLogin: true,
  });
}

function handleOnFailure() {}

export default function GoogleButton() {
  return (
    <GoogleLogin
      clientId="836600659281-eeutvpmf60kb2f2jfhcju5kfnebbsuu2.apps.googleusercontent.com"
      buttonText="Login with Google"
      onSuccess={handleGoogleOAuthLogin}
      onFailure={handleOnFailure}
      cookiePolicy="single_host_origin"
    />
  );
}
