import React from 'react';
import ReactDom from 'react-dom';
import ActivityCard from '../components/activities/activity_card';

class ViewActivities extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activities: context.activities,
            ownedActivities: context.owned_activities,
            pastActivities: context.past_activities
        };

        console.log(this.state);
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <div className="col s12 m2 margin-top">
                        <center>
                            <a href="/activities/create/" className="btn">Create new</a>
                            <p>
                                <a href="/activities/search/">Search activities</a>
                            </p>
                        </center>
                    </div>

                    <div className="col s12 m8 margin-top">
                        <ul className="tabs">
                            <li className="tab col s4">
                                <a href="#all">Activities</a>
                            </li>
                            <li className="tab col s4">
                                <a href="#owned">Created activities</a>
                            </li>
                            <li className="tab col s4">
                                <a href="#past">Past activities</a>
                            </li>
                        </ul>
                        
                        <div id="all">
                            {this.state.activities.map((element, index) => {
                                return <ActivityCard activity={element} key={index} />
                            })}
                        </div>

                        <div id="owned">
                            {this.state.activities.map((element, index) => {
                                return <ActivityCard activity={element} key={index} />
                            })}
                        </div>

                        <div id="past">
                            {this.state.pastActivities.map((element, index) => {
                                return <ActivityCard activity={element} key={index} />
                            })}
                        </div>
                    </div>

                </div>
            </div>
        );
    }
}

ReactDom.render(
    <ViewActivities />,
    document.getElementById('root')
);