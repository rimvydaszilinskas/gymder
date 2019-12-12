import React from 'react';


const GroupSideNavigation = (props) => {
    return (
        <ul className="collection with-headers">
            <li className="collection-item">
                <span className="lead">Navigation</span>
            </li>
            <a href={`/groups/${props.uuid}/`} className="collection-item">Home</a>
            <a href={`/groups/${props.uuid}/activities/`} className="collection-item">Activities</a>
            <a href={`/groups/${props.uuid}/members/`} className="collection-item">Members</a>
            {props.is_owner ? <a href="#" onClick={props.callback} className="collection-item">Delete</a>: null}
        </ul>
    );
};

export default GroupSideNavigation;