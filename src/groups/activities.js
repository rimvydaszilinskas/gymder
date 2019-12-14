import React from 'react';
import ReactDom from 'react-dom';
import GroupSideNavigation from '../components/groups/sidemenu';
import ActivityCard from '../components/activities/activity_card';

class GroupActivities extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            group: context.group,
            user: context.user,
            activities: context.activities
        };

        this.deleteGroup = this.deleteGroup.bind(this);
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
                                        {this.state.activities.length} activities | Created by <a href="#">{this.state.group.user.username}</a>
                                    </span>
                                </div>
                            </div>
                        </div>

                        {this.state.activities.length !== 0 ? 
                            this.state.activities.map((activity, index) => {
                                return <ActivityCard key={index} activity={activity}/>;
                            })
                        : <div className="card-panel">
                            <span>No activities found</span>
                        </div>}
                    </div>

                    <div className="col m2 s12 margin-top">
                        <center>
                            <a href={`/groups/${this.state.group.uuid}/activities/create/`} className="btn">Create new</a>
                        </center>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

ReactDom.render(
    <GroupActivities />,
    document.getElementById('root')
);
