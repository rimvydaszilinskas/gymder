import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';
import ActivitySideNavigation from '../components/activities/sidemenu';


class ActivityAttendees extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activity: context.activity,
            user: context.user
        }

        this.determineStatusMessage = this.determineStatusMessage.bind(this);
        this.denyRequest = this.denyRequest.bind(this);
        this.approveRequest = this.approveRequest.bind(this);

        console.log(this.state);
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

    denyRequest(uuid) {
        fetch(`/api/activities/${this.state.activity.uuid}/requests/${uuid}/`, {
            method: 'DELETE',
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
                console.log('ooook');
                let requestIndex = this.state.activity.requests.findIndex((element) => {
                    return element.uuid === uuid;
                });

                let request = this.state.activity.requests[requestIndex];
                request.status = 'denied';

                let activity = this.state.activity;
                activity.requests[requestIndex] = request;

                this.setState({
                    activity: activity
                });
            }
		}).catch(e => {
            console.log(e);
			alert('Error denying response');
		});
    }

    approveRequest(uuid) {
        fetch(`/api/activities/${this.state.activity.uuid}/requests/${uuid}/`, {
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
                let requestIndex = this.state.activity.requests.findIndex((element) => {
                    return element.uuid === uuid;
                });

                let request = this.state.activity.requests[requestIndex];
                request.status = 'approved';

                let activity = this.state.activity;
                activity.requests[requestIndex] = request;

                this.setState({
                    activity: activity
                });
            } else if(response.status === 400) {
                alert('Activity is fully booked!');
            }
		}).catch(e => {
            console.log(e);
			alert('Error denying response');
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
                            is_owner={false}
                            />
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
                                        {this.state.activity.public ? 'Public' : 'Private'} {this.state.activity.is_group ? '| Group' : ''} {this.determineStatusMessage()} | Hosted by <a href="">{this.state.activity.user.username}</a>
                                    </span>
                                </div>
                            </div>
                        </div>

                        <div className="card-panel margin-top">
                            <div className="row no margin">
                                <h5>Attendees</h5>

                                {this.state.activity.approved_requests !== 0 ? 
                                    <ul className="collection">
                                        {this.state.activity.requests.filter((req) => {
                                            return req.status === 'approved';
                                        }).map((request, index) => {
                                            return (
                                                <li className="collection-item avatar" key={index}>
                                                    <a href="#">
                                                        <i className="material-icons circle green">person</i>
                                                    </a>
                                                    <span className="title">{request.user.username}</span>
                                                    <p>{request.user.email}</p>
                                                    <p>{request.status}</p>
                                                    {
                                                        this.state.user.uuid === this.state.activity.user.uuid &&
                                                        <div className="secondary-content">
                                                            <a href="#" onClick={() => {this.approveRequest(request.uuid)}}>
                                                                <i className="material-icons">check</i>
                                                            </a>
                                                            <a href="#" onClick={() => {this.denyRequest(request.uuid)}}>
                                                                <i className="material-icons">clear</i>
                                                            </a>
                                                        </div>
                                                    }
                                                </li>
                                            );
                                        })}
                                    </ul>: <span>No attendees</span>}
                                
                            </div>
                        </div>

                        <div className="card-panel margin-top">
                            <div className="row no margin">
                                <h5>Requests</h5>
                                {this.state.activity.requests.filter(req => {
                                    return req.status !== 'approved';
                                }).length !== 0 ? 
                                    <ul className="collection">
                                        {this.state.activity.requests.filter(req => {
                                            return req.status !== 'approved';
                                        }).map((request, index) => {
                                            return (
                                                <li className="collection-item avatar" key={index}>
                                                    <a href="#">
                                                        <i className="material-icons circle green">person</i>
                                                    </a>
                                                    <span className="title">{request.user.username ? request.user.username : 'No username'}</span>
                                                    <p>{request.user.email}</p>
                                                    <p>{request.status}</p>
                                                    {
                                                        this.state.user.uuid === this.state.activity.user.uuid &&
                                                        <div className="secondary-content">
                                                            <a href="#" onClick={() => {this.approveRequest(request.uuid)}}>
                                                                <i className="material-icons">check</i>
                                                            </a>
                                                            <a href="#" onClick={() => {this.denyRequest(request.uuid)}}>
                                                                <i className="material-icons">clear</i>
                                                            </a>
                                                        </div>
                                                    }
                                                </li>
                                            );
                                        })}
                                    </ul> : <span>No requests</span>}
                            </div>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        )
    }
}

ReactDom.render(
    <ActivityAttendees />,
    document.getElementById('root')
);
