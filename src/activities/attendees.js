import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';
import ActivitySideNavigation from '../components/activities/sidemenu';


class ActivityAttendees extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activity: context.activity
        }

        this.determineStatusMessage = this.determineStatusMessage.bind(this);
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
                                    <React.Fragment>
                                        {this.state.activity.requests.map((request, index) => {
                                            // place code here
                                        })}
                                    </React.Fragment>: <span>No attendees</span>}
                                
                            </div>
                        </div>

                        <div className="card-panel margin-top">
                            <div className="row no margin">
                                <h5>Requests</h5>
                                {this.state.activity.requests.length !== 0 ? 
                                    <React.Fragment>
                                        {this.state.activity.requests.map((request, index) => {
                                            //place code here
                                        })}
                                    </React.Fragment> : <span>No requests</span>}
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
