import React from 'react';


let ActivityCard = (props) => {
    let activityType = props.activity.is_group ? 'Group' : 'Individual';
    let publicStatus = props.activity.public ? 'Public' : 'Private';
    let needApproval = props.activity.needs_approval ? ' | Needs approval' : '';

    return (
        <div className="card">
            <div className="card-content">
                <span className="card-title">{props.activity.title}</span>
                <p>
                    <i>{props.activity.formatted_dates}</i>
                </p>
                <p>
                    <i>{props.activity.address ? props.activity.address.address : '-'}</i>
                </p>
                <p><b>{activityType}</b> activity | <b>{props.activity.number_of_attendees}</b> attendees | <b>{publicStatus}</b> {needApproval}</p>
            </div>

            <div className="card-action">
                <a href={`/activities/${props.activity.uuid}/`}>View activity</a>
            </div>
        </div>
    );
};

export default ActivityCard;
