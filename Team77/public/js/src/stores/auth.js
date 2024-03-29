var React = require('react/addons');
var Reflux = require('reflux');
var Actions = require('../actions');
var request = require('superagent');
var StatusTypes = require('status-types');
var ErrorActions = require('../actions-error');

var AuthStore = Reflux.createStore({
    listenables: [Actions],
    getDefaultData: function() {
        this.data = {
            currentUser: {
                user_id: 0
            },
            errorMessages: {
                login: null,
                signup: null
            }
        }
        return this.data;
    },
    onGetCurrentUser: function() {
        request
            .get('/api/auth')
            .end(function(err, res) {
                //user not logged in, set current user to null/redirect to index
                if (res.status === StatusTypes.unauthorized) {
                    console.log('user not logged in');
                    this.data.currentUser = {
                        user_id: 0
                    };
                }
                //user logged in, set current user to user
                if (res.status === StatusTypes.ok) {
                    console.log('user is logged in');
                    this.data.currentUser = res.body;
                }
                this.trigger(this.data);
            }.bind(this));
    },
    onLogin: function(login_data) {
        request
            .post('/api/auth')
            .send(login_data)
            .end(function(err, res) {
                if (res.status === StatusTypes.unauthorized) {
                    console.log('user failed to log in');
                    // this.data.errorMessages.login = res.body.message;
                    ErrorActions.throwError({
                        message: res.body.message
                    });
                    this.trigger(this.data);
                    return;
                }
                //logged in, set current user to user/update ui
                if (res.status === StatusTypes.ok) {
                    // console.log(res.body)
                    console.log('user logged in successfully');
                    this.data.currentUser = res.body;
                    this.data.errorMessages.login = null;
                    this.trigger(this.data);
                    return;
                }
                ErrorActions.throwUnknownStatus(res);
            }.bind(this));
    },
    onLogout: function() {
        request
            .del('/api/auth')
            .end(function(err, res) {
                //logged out, set current user to null/update ui/redirect to index
                if (res.status === StatusTypes.noContent || res.status === StatusTypes.unauthorized) {
                    console.log('user logged out successfully');
                    this.data.currentUser = {
                        user_id: 0
                    };
                    this.trigger(this.data);
                    return;
                }
                ErrorActions.throwUnknownStatus(res);
            }.bind(this));
    },
    onSignup: function(register_data) {
        console.log('registering!');
        request
            .post('/api/auth/register')
            .send(register_data)
            .end(function(err, res) {
                console.log('GOT A RESPONSE FROM REGISTERING');
                if (res.status === StatusTypes.content) {
                    console.log('user registered/logged in successfully');
                    this.data.currentUser = res.body;
                    this.data.errorMessages.signup = null;
                    this.trigger(this.data);
                    return;
                }
                if (res.status === StatusTypes.badRequest) {
                    console.log('user failed to be registered');
                    console.log(res.body.message);
                    ErrorActions.throwError({
                        message: res.body.message
                    });
                    // this.data.errorMessages.signup = res.body.message;
                    this.trigger(this.data);
                    return;
                }
                ErrorActions.throwUnknownStatus(res);
            }.bind(this));
    }
});

module.exports = AuthStore;
