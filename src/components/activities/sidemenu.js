import React from 'react';


const ActivitySideNavigation = (props) => {
    let elements = [
        <a href={`/activities/${props.uuid}/`} key="home" className="collection-item">Home</a>,
        <a href={`/activities/${props.uuid}/attendees/`} key="attendees" className="collection-item">Attendees</a>
    ];

    if (props.is_owner) {
        elements.push(
            <a href="#" onClick={props.deleteCallback ? props.deleteCallback : () => {}} key='settings' className="collection-item">Delete</a>
        );
    }

    return (
        <ul className="collection with-headers">
            <li className="collection-item">
                <span className="lead">Navigation</span>
            </li>
            {elements}
        </ul>
    )
};

export default ActivitySideNavigation;
