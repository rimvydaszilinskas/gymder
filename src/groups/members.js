import React from 'react';
import ReactDom from 'react-dom';
import GroupSideNavigation from '../components/groups/sidemenu';
import getCookie from '../utils/get_cookie';


class MembersView extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            group: context.group,
            user: context.user,
            memberships: context.memberships,
            addUserText: '',
        };

        console.log(this.state);

        this.deleteGroup = this.deleteGroup.bind(this);
        this.addUser = this.addUser.bind(this);
        this.handleAddUserInput = this.handleAddUserInput.bind(this);
        this.approveMember = this.approveMember.bind(this);
        this.declineMember = this.declineMember.bind(this);
    }

    deleteGroup() {
        let confirmation = confirm('Are you sure you want to delete?');

        if(!confirmation) {
            return;
        }

        fetch(`/api/groups/${this.state.group.uuid}/`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                user: this.state.addUserText
            })
        }).then(response => {
            if(response.status === 200) {
                window.location.replace('/groups/');
            } else {
                alert('Something went wrong');
            }
        }).catch(e => {
            console.log(e);
            alert('Cannot add member!')
        });
    }

    handleAddUserInput(e) {
        this.setState({
            addUserText: e.target.value
        });
    }

    addUser() {
        if(this.state.addUserText.length < 5) {
            return;
        }

        fetch(`/api/groups/${this.state.group.uuid}/memberships/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                user: this.state.addUserText
            })
        }).then(response => {
            if(response.status === 201) {
                response.json().then(responseJSON => {
                    let group = this.state.group;
                    let memberships = this.state.memberships;

                    group.number_of_users++;
                    memberships.push(responseJSON);

                    this.setState({
                        group: group,
                        addUserText: '',
                        memberships: memberships
                    });
                });
            } else if(response.status === 200) {
                alert('User already in the group');
            }else if (response.status === 404) {
                alert('User not found');
            }
        }).catch(e => {
            console.log(e);
            alert('Cannot add member!')
        });
    }

    approveMember(uuid) {
        fetch(`/api/memberships/${uuid}/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                status: 'approved'
            })
        }).then(response => {
            if(response.status === 200) {
                let memberships = this.state.memberships;
                let index = memberships.findIndex(membership => membership.uuid === uuid);
                let membership = memberships[index];

                membership.status = 'approved';
                memberships[index] = membership;

                this.setState({
                    memberships: memberships
                });
            }
        }).catch(e => {
            alert('Error approving request');
        });
    }

    declineMember(uuid) {
        fetch(`/api/memberships/${uuid}/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                status: 'denied'
            })
        }).then(response => {
            if(response.status === 200) {
                let memberships = this.state.memberships;
                let index = memberships.findIndex(membership => membership.uuid === uuid);
                let membership = memberships[index];

                membership.status = 'denied';
                memberships[index] = membership;

                this.setState({
                    memberships: memberships
                });
            }
        }).catch(e => {
            alert('Error denying request');
        });
    }

    render() {
        return (
            <React.Fragment>
                <div className="row">
                    <div className="col s1 hide-on-small-only"></div>
                    <div className="col m2 s12">
                        <GroupSideNavigation 
                            uuid={this.state.group.uuid}
                            is_owner={this.state.group.user.uuid === this.state.user.uuid}
                            callback={this.deleteGroup}
                            />
                    </div>

                    <div className="col m6 s12">
                        <div className="card-panel margin-top">
                            <div className="row">
                                <div className="s12">
                                    <h3>{this.state.group.title}</h3>

                                    <span className="helper-text">
                                        {this.state.memberships.length} members | Created by <a href="#">{this.state.group.user.username}</a>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="row">
                            <ul className="tabs">
                                <li className="tab col s4">
                                    <a href="#approved-members">Approved</a>
                                </li>
                                <li className="tab col s4">
                                    <a href="#pending-members">Pending</a>
                                </li>
                                <li className="tab col s4">
                                    <a href="#all-members">All</a>
                                </li>
                            </ul>
                        </div>

                        <div id="approved-members">
                            {this.state.memberships.length !== 0 ?
                                this.state.memberships.filter((membership) => {
                                    return membership.status === 'approved';
                                }).map((membership, index) => {
                                    return (
                                        <div className="card" key={index}>
                                            <div className="card-content">
                                                <span className="card-title">{membership.user.username ? membership.user.username : membership.user.email}</span>

                                                <p>
                                                    Status: {membership.status}
                                                </p>
                                            </div>
                                            
                                            {this.state.user.uuid === this.state.group.user.uuid &&
                                                <div className="card-action">
                                                    <a className="btn" onClick={() => this.approveMember(membership.uuid)}>Approve</a> 
                                                    <a className="btn btn-space-left" onClick={() => this.declineMember(membership.uuid)}>Decline</a>
                                                </div>
                                            }
                                        </div>
                                    );
                                })
                                : <div className="card-panel">
                                    <span>No members</span>
                                </div>
                            }
                        </div>

                        <div id="pending-members">
                            {this.state.memberships.length !== 0 ?
                                this.state.memberships.filter((membership) => {
                                    return membership.status === 'pending';
                                }).map((membership, index) => {
                                    return (
                                        <div className="card" key={index}>
                                            <div className="card-content">
                                                <span className="card-title">{membership.user.username ? membership.user.username : membership.user.email}</span>

                                                <p>
                                                    Status: {membership.status}
                                                </p>
                                            </div>
                                            
                                            {this.state.user.uuid === this.state.group.user.uuid &&
                                                <div className="card-action">
                                                    <a className="btn" onClick={() => this.approveMember(membership.uuid)}>Approve</a> 
                                                    <a className="btn btn-space-left" onClick={() => this.declineMember(membership.uuid)}>Decline</a>
                                                </div>
                                            }
                                        </div>
                                    );
                                })
                                : <div className="card-panel">
                                    <span>No members</span>
                                </div>
                            }
                        </div>

                        <div id="all-members">
                            {this.state.memberships.length !== 0 ?
                                this.state.memberships.map((membership, index) => {
                                    return (
                                        <div className="card" key={index}>
                                            <div className="card-content">
                                                <span className="card-title">{membership.user.username ? membership.user.username : membership.user.email}</span>

                                                <p>
                                                    Status: {membership.status}
                                                </p>
                                            </div>
                                            
                                            {this.state.user.uuid === this.state.group.user.uuid &&
                                                <div className="card-action">
                                                    <a className="btn" onClick={() => this.approveMember(membership.uuid)}>Approve</a> 
                                                    <a className="btn btn-space-left" onClick={() => this.declineMember(membership.uuid)}>Decline</a>
                                                </div>
                                            }
                                        </div>
                                    );
                                })
                                : <div className="card-panel">
                                    <span>No members</span>
                                </div>
                            }
                        </div>
                    </div>

                    <div className="col m2 s12">
                        <div className="card-panel margin-top">
                            <div className="row">
                                <span className="helper-text">Add member</span>
                                <div className="input-field">
                                    <input className="validate" type="text" id="user" value={this.state.addUserText} onChange={this.handleAddUserInput}></input>
                                    <label htmlFor="user">Username or email</label>
                                </div>
                                <center>
                                    <button className="btn" onClick={this.addUser}>Add</button>
                                </center>
                            </div>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}


ReactDom.render(
    <MembersView />,
    document.getElementById('root')
);
