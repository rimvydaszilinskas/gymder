import React from 'react';
import ReactDom from 'react-dom';
import ActivityCard from '../components/activities/activity_card';

class Profile extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            user: context.user,
            activities: context.owned_activities
        };
    }

    render() {
        return (
            <div className="container">
                <div className="col m2 hide-on-small-only"></div>
                <div className="col m8 s12 margin-top">
                    <center>
                        <h3>
                            <i className="material-icons large circle green">person</i>
                            <br/>{this.state.user.first_name} {this.state.user.last_name}
                        </h3>

                        <p>
                            @{this.state.user.username} | {this.state.user.email}
                        </p>
                        
                        <p>
                            {
                                this.state.user.tags.map((tag, index) => {
                                    return <a key={index} href={`/activities/search/${tag.uuid}/`}>#{tag.title} </a>
                                })
                            }
                        </p>

                        <h5>Activities</h5>
                        
                    </center>

                    {this.state.activities.length === 0 ? <h4>No activities</h4> : this.state.activities.map((activity, index) => {
                            return <ActivityCard activity={activity} key={index} />;
                        })
                    }
                </div>
            </div>
        );
    }
}

ReactDom.render(
    <Profile />,
    document.getElementById('root')
);
