import React from 'react';
import ReactDom from 'react-dom';
import ActivityCard from '../components/activities/activity_card';

class TagSearch extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            activities: context.activities,
            tag: context.tag
        };

        console.log(this.state);
    }

    render() {
        return (
            <div className="container margin-top">
                <div className="row">
                    <center>
                        <h3>#{this.state.tag.title}</h3>
                    </center>
                </div>

                <div className="row">
                    {
                        this.state.activities.length === 0 ? 
                        <center>
                            No results
                        </center>: this.state.activities.map((activity, index) => {
                            return <ActivityCard activity={activity} key={index} />
                        })
                    }
                </div>
            </div>
        );
    }
}

ReactDom.render(
    <TagSearch />,
    document.getElementById('root')
);
