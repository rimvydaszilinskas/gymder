import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';

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
			posts_error: false
		}
		
		this.fetchPosts = this.fetchPosts.bind(this);
		this.fetchPosts()
	}
	
	fetchPosts() {
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
			response.json().then(responseJSON => {
				this.setState({
					posts: responseJSON
				})
			});
		}).catch(e => {
			this.setState({
				posts_error: true
			})
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

    render() {
        return (
            <React.Fragment>
                <div className="row">
					<div className="col m1 hide-on-small-only"></div>
                    <div className="col m2 s12">
                        <h1>Navi</h1>
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
                                        {this.state.activity.public ? 'Public' : 'Private'} {this.state.activity.is_group ? '| Group' : ''} | Hosted by <a href="">{this.state.activity.user.username}</a>
                                    </span>
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
                        </div>

						<div className="card-panel">
							<div className="row">
								<div className="col s2">
									<img className="circle responsive-img profile-img" src="/static/images/default_profile.jpeg"></img>
								</div>
								<div className="col s10">
									<div className="input-field">
										<textarea className="materialize-textarea" id="post"></textarea>
										<label htmlFor="post">Post something</label>
									</div>
								</div>
								<center>
									<button className="btn">Post</button>
								</center>
							</div>
						</div>

						{
							this.state.posts_loaded ? 
								this.state.posts_error ? <div className="card-panel">Error loading posts</div> : 
									this.state.posts.map((post, index) => {
										return <div className="card-panel" key={index}>
											<div className="row">
												<div className="col s2">
													<img className="circle responsive-img profile-img" src="/static/images/default_profile.jpeg"></img>
												</div>
												<div className="col s10">
													<a className="author" href="#">{post.user.username}</a>
													{this.formatDescription(post.body)}
												</div>
											</div>
										</div>
									})
								 : <div className="card-panel">Loading</div>
						}
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

ReactDom.render(
    <PreviewActivity />,
    document.getElementById('root')
);