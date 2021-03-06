import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';
import ActivitySideNavigation from '../components/activities/sidemenu';
import StatusButtons from '../components/activities/status_buttons';


class PreviewActivity extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: context.user,
            is_owner: context.is_owner,
            created: context.created,
			activity: context.activity,
			posts: [],
			posts_loaded: false,
            posts_error: false,
            user_request: context.user_request,
            post: {
                body: ''
            },
            tag: ''
        };
        
        this.fetchPosts = this.fetchPosts.bind(this);
        this.handlePostInput = this.handlePostInput.bind(this);
        this.handleSavePostClick = this.handleSavePostClick.bind(this);
        this.handleStatusButtonClick = this.handleStatusButtonClick.bind(this);
        this.determineStatusMessage = this.determineStatusMessage.bind(this);
        this.deleteActivity = this.deleteActivity.bind(this);
        this.handleDeleteTags = this.handleDeleteTags.bind(this);
        this.handleTagInput = this.handleTagInput.bind(this);
        this.handleTagFormSubmit = this.handleTagFormSubmit.bind(this);

        this.fetchPosts()
    }
    
    determineStatusMessage() {
        // Return status message for this activity
        let value = '';

        if (!this.state.activity.is_group) {
            if (this.state.activity.approved_requests === 1) {
                value = 'Fully booked'
            }
            else {
                value = '1 spot available'
            }
        } else {
            if (this.state.activity.approved_requests >= this.state.activity.max_attendees) {
                value = 'Fully booked';
            } else {
                let spots_left = this.state.activity.max_attendees - this.state.approved_requests;
                let plural = spots_left === 1 ? '' : 's';

                value = `${spots_left} spot${plural} available`;
            }
        }

        return ` | ${value}`; 
    }
	
	fetchPosts() {
        // fetch posts for the activity async
		fetch(`/api/activities/${this.state.activity.uuid}/posts/`, {
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
            
            if(response.status === 200) {
                response.json().then(responseJSON => {
                    this.setState({
                        posts: responseJSON
                    })
                });
            }
			
		}).catch(e => {
			this.setState({
				posts_error: true
			})
		});
    }
    
    handlePostInput(e) {
        let post = this.state.post;

        post.body = e.target.value;

        this.setState({
            post: post
        });
    }

    handleSavePostClick(e) {
        // handle saving of the post
        e.preventDefault();

        if(this.state.post.body.length < 5) {
            return;
        }

        fetch(`/api/activities/${this.state.activity.uuid}/posts/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                body: this.state.post.body
            })
        }).then(response => {
            if(response.status===200 || response.status===201) {
                response.json().then(responseJSON => {
                    let posts = this.state.posts;
                    posts.unshift(responseJSON);

                    this.setState({
                        posts: posts,
                        post: {
                            body: ''
                        }
                    });
                });
            } else {
                alert('There was an error posting')
            }
        }).catch(e => {
            console.log(e);
            alert('Something went wrong while posting');
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

    handleStatusButtonClick() {
        fetch(`/api/activities/${this.state.activity.uuid}/requests/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => {
            response.json().then(responseJSON => {
                if(responseJSON.deleted) {
                    this.setState({
                        user_request: null
                    });
                } else if (responseJSON.detail) {
                    if (response.status === 403) {
                        alert('Activity fully booked');
                    }
                } else {
                    console.log(responseJSON);
                    this.setState({
                        user_request: responseJSON
                    });
                }
            });
        }).catch(e => {
            console.log(e);
        });
    }

    deleteActivity() {
        let confirmed = confirm('Are you sure you want to delete this activity?');

        if(!confirmed) {
            return;
        }

        fetch(`/api/activities/${this.state.activity.uuid}/`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).then(response => {
            if(response.status === 200) {
                window.location.replace('/activities/');
            }
        }).catch(e => {
            alert('error deleting activity');
        });
    }

    handleDeleteTags(e, uuid) {
        fetch(`/api/activities/${this.state.activity.uuid}/tags/`, {
            method: 'DELETE',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                uuid: uuid
            })
        }).then(response => {
            if(response.status === 200) {
                let activity = this.state.activity;
                let tags = activity.tags;

                tags = tags.filter((value) => {
                    return value.uuid !== uuid;
                });

                activity.tags = tags;

                this.setState({
                    activity: activity
                });
            } else {
                alert('Error removing tag');
            }
        }).catch(err => {
            alert('Error removing tag');
        });
    }

    handleTagInput(e) {
        this.setState({
            tag: e.target.value
        });
    }

    handleTagFormSubmit(e) {
        e.preventDefault();

        fetch(`/api/activities/${this.state.activity.uuid}/tags/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                title: this.state.tag
            })
        }).then(response => {
            if(response.status === 200) {
                response.json().then(res => {
                    let activity = this.state.activity;
                    let tags = activity.tags;

                    tags.push(res);
                    activity.tags = tags;

                    this.setState({
                        activity: activity,
                        tag: ''
                    });
                })
            }
        }).catch(e => {
            console.log(e);
            alert('Error adding tag');
        });
    }

    render() {
        return (
            <React.Fragment>
                <div className="row">
					<div className="col m1 hide-on-small-only"></div>
                    <div className="col m2 s12">
                        <ActivitySideNavigation 
                            uuid={this.state.activity.uuid} 
                            is_owner={this.state.user.uuid === this.state.activity.user.uuid}
                            deleteCallback={this.deleteActivity}
                            />
                        {this.state.user.uuid !== this.state.activity.user.uuid &&
                            <StatusButtons 
                                need_approval={this.state.activity.needs_approval} 
                                request={this.state.user_request}
                                onClick={this.handleStatusButtonClick}
                                />
                        }
                    </div>
                    <div className="col m6 s12">
                        <div className="card-panel margin-top">
                            <div className="row">
                                <div className="col s2">
                                    <center>
                                        <span className="event-month">{this.state.activity.formatted_month_short}</span><br/>
                                        <span className="event-day">{this.state.activity.formatted_day_number}</span>
                                    </center>
                                </div>
                                <div className="col s10">
                                    <h3 className="no-margin-top">{this.state.activity.title}</h3>

                                    <span className="helper-text">
                                        {this.state.activity.public ? 'Public' : 'Private'} {this.state.activity.is_group ? '| Group' : ''} {this.determineStatusMessage()} | Hosted by <a href={`/users/profile/${this.state.activity.user.uuid}/`}>{this.state.activity.user.username}</a>
                                    </span>

                                    {this.state.activity.group && 
                                        <span className="helper-text"><br/>Group: <a href={`/groups/${this.state.activity.group.uuid}`}>{this.state.activity.group.title}</a></span>
                                    }
                                </div>
                            </div>

                            <hr/>

                            <div className="row no-margin">
                                <div className="col s1">
                                    <i className="small material-icons">date_range</i>
                                </div>
                                <div className="col s11">
                                    <span className="datetime">
                                        {this.state.activity.formatted_day_long},&nbsp;	
                                        {this.state.activity.formatted_day_number} {this.state.activity.formatted_month_long} {this.state.activity.formatted_year}
                                    </span>
                                </div>
                            </div>
                            <hr/>

                            <div className="row no-margin">
                                <div className="col s1">
                                    <i className="small material-icons">timer</i>
                                </div>
                                <div className="col s11">
                                    <span className="datetime">{this.state.activity.duration} mins</span>
                                </div>
                            </div>
                            <hr/>

                            <div className="row no-margin clickable">
                                <div className="col s1">
                                    <i className="small material-icons">location_on</i>
                                </div>
                                <div className="col s11">
                                    <span className="datetime">{this.state.activity.address.address}</span>
                                </div>
                            </div>
                            <hr/>

                            <div className="row no-margin">
                                <div className="col s1">
                                    <i className="small material-icons">short_text</i>
                                </div>
                                <div className="col s11">
                                    {this.formatDescription(this.state.activity.description)}
                                </div>
                            </div>
                            <hr/>

                            <div className="row no-margin">
                                <div className="col s1">
                                    <i className="small material-icons">format_align_justify</i>
                                </div>
                                <div className="col s11">
                                    {this.state.activity.tags.map((tag, index) => {
                                        return <a key={index} href={`/activities/search/${tag.uuid}/`}>#{tag.title} </a>;
                                    })}
                                </div>
                            </div>
                            <hr/>
                        </div>

						<div className="card-panel">
							<div className="row">
								<div className="col s2">
									<img className="circle responsive-img profile-img" src="/static/images/default_profile.jpeg"></img>
								</div>
								<div className="col s10">
									<div className="input-field">
										<textarea className="materialize-textarea" id="post" value={this.state.post.body} onChange={this.handlePostInput}></textarea>
										<label htmlFor="post">Post something</label>
									</div>
								</div>
								<center>
									<button className="btn" onClick={this.handleSavePostClick}>Post</button>
								</center>
							</div>
						</div>

						{   // This is a bit of complex logic to display the appropriate message/posts
							this.state.posts_loaded ? 
								this.state.posts_error ? <div className="card-panel">Error loading posts</div> : 
									this.state.posts.map((post, index) => {
										return <div className="card-panel" key={index}>
											<div className="row">
												<div className="col s2">
													<img className="circle responsive-img profile-img" src="/static/images/default_profile.jpeg"></img>
												</div>
												<div className="col s10">
													<a className="author" href={`/user/profile/${post.user.uuid}/`}>{post.user.username}</a> <br />
                                                    <span className="secondary">{post.date}</span> <br />
													{this.formatDescription(post.body)}
												</div>
											</div>
										</div>
									})
								 : <div className="card-panel">Loading</div>
						}

                    </div>
                    {
                        this.state.user.uuid === this.state.activity.user.uuid &&
                        <div className="col m2 s12">
                            <center>
                                <h4>Tags</h4>
                            </center>
                            
                            <div className="row">
                            {
                                this.state.activity.tags.map((tag, index) => {
                                    return (
                                        <div className="chip" key={index}>
                                            <span>{tag.title}</span>
                                            <i className="material-icons click" onClick={(e) => {this.handleDeleteTags(e, tag.uuid)}}>close</i>
                                        </div>
                                    );
                                })
                            }
                            </div>

                            <div className="row padding">
                                <form ref="form" onSubmit={this.handleTagFormSubmit}>
                                    <div className="row input-field">
                                        <input type="text" className="validate" id="tag" value={this.state.tag} onChange={this.handleTagInput}></input>
                                        <label htmlFor="tag">+Tag</label>
                                    </div>

                                    <center>
                                        <button className="btn" type="submit">Submit</button>
                                    </center>
                                </form>
                            </div>
                            
                        </div>
                    }
                </div>
            </React.Fragment>
        );
    }
}

ReactDom.render(
    <PreviewActivity />,
    document.getElementById('root')
);
