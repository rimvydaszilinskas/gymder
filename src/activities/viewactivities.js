import React from 'react';
import ReactDom from 'react-dom';
import ActivityCard from '../components/activities/activity_card';

class ViewActivities extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activities: context.activities
        }
    }

    render() {
        return (
            <React.Fragment>
                <div className="row">
                    <div className="col s12 m7">
                        {this.state.activities.map((element, index) => {
                            return <ActivityCard activity={element} key={index} />
                        })}
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

ReactDom.render(
    <ViewActivities />,
    document.getElementById('root')
);