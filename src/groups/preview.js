import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';
import GroupSideNavigation from '../components/groups/sidemenu';

class GroupView extends React.Component {
    constructor(props) {
        super(props);
        
        this.state = {
            group: context.group,
            user: context.user,
            post: '',
            posts: [],
            posts_loaded: false,
            posts_error: false,
            addUserText: '',
        };

        this.handlePostInput = this.handlePostInput.bind(this);
        this.handleSavePostClick = this.handleSavePostClick.bind(this);
        this.fetchPosts = this.fetchPosts.bind(this);
        this.handleAddUserInput = this.handleAddUserInput.bind(this);
        this.addUser = this.addUser.bind(this);
        this.deleteGroup = this.deleteGroup.bind(this);

        this.fetchPosts();
    }

    handlePostInput(e) {
        this.setState({
            post: e.target.value
        });
    }

    handleSavePostClick(e) {
        e.preventDefault();

        if(this.state.post.length < 5) {
            return;
        }

        fetch(`/api/groups/${this.state.group.uuid}/posts/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                body: this.state.post
            })
        }).then(response => {
            if(response.status === 200 || response.status === 201) {
                response.json().then(responseJSON => {
                    let posts = this.state.posts;

                    posts.unshift(responseJSON);

                    this.setState({
                        posts: posts,
                        post: ''
                    });
                });
            }
        }).catch(e => {
            alert('Something went wrong while posting');
        });
    }

    fetchPosts() {
        // fetch posts for the activity async
		fetch(`/api/groups/${this.state.group.uuid}/posts/`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            }
        }).then(response => {
			this.setState({
				posts_loaded: true
			});
			response.json().then(responseJSON => {
				this.setState({
					posts: responseJSON
                });
			});
		}).catch(e => {
			this.setState({
				posts_error: true
			});
		});
    }

    formatDescription(description) {
        // do formatting of description to preview
        if (description) {
            let raw = description.split('\n').map((i, index) => <p key={index}>{i}</p>)
            return raw;
        }

        return description;
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

                    group.number_of_users++;

                    this.setState({
                        group: group,
                        addUserText: ''
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
                                        {this.state.group.number_of_users} members | Created by <a href="#">{this.state.group.user.username}</a>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="card-panel">
                            <div className="row">
                                <div className="col s2">
                                    <img className="circle responsive-img profile-img" src="/static/images/default_profile.jpeg"></img>
                                </div>
                                <div className="col s10">
                                    <div className="input-field">
                                        <textarea className="materialize-textarea" id="post" value={this.state.post} onChange={this.handlePostInput}></textarea>
                                        <label htmlFor="post">Post something</label>
                                    </div>
                                </div>
                                <center>
                                    <button className="btn" onClick={this.handleSavePostClick}>Post</button>
                                </center>
                            </div>
                        </div>

                        {
                            this.state.posts_loaded ? 
                                this.state.posts_error ? <div className="card-panel">Error loading posts</div>:
                                    this.state.posts.map((post, index) => {
                                        return (
                                            <div className="card-panel" key={index}>
                                                <div className="row">
                                                    <div className="col s2">
                                                        <img className="circle responsive-img profile-img" src="/static/images/default_profile.jpeg"></img>
                                                    </div>
                                                    <div className="col s10">
                                                        <a className="author" href="#">{post.user.username}</a> <br />
                                                        <span className="secondary">{post.date}</span> <br />
                                                        {this.formatDescription(post.body)}
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    }) : <div className="card-panel">Loading</div>
                        }
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
    <GroupView />,
    document.getElementById('root')
);
