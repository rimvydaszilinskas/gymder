import React from 'react';
import ReactDom from 'react-dom';

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
                            return (
                                <div className="card">
                                    <span className="activity">{element.title}</span>
                                    <div className="card-content">
                                       <span className="date">{element.formatted_dates}</span><br/>
                                       <span className="address">{element.address.address}</span><br/>
                                    </div>
                                    <div className="card-action">
                                        <a href={`/activities/${element.uuid}/`}>Go to activity</a>
                                    </div>
                                </div>
                            )
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