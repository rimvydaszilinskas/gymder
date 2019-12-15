import React from 'react';

let GroupCard = (props) => {
    /* Card module for displaying groups
     * Pass group in props
     * Mandatory fields for group:
     * - title
     * - uuid
     * - public
     * - username
     * - number_of_users
    */
    let isPublic = props.group.public ? 'Public': 'Private';
    let members = '';
    if(props.group.number_of_users === 0) {
        members = 'No users';
    } else if(props.group.number_of_users === 1) {
        members = props.group.number_of_users.toString() + ' member';
    } else {
        members = props.group.number_of_users.toString() + ' members';
    }
    let username = props.group.user.username ? props.group.user.username : props.group.user.email;
    
    return (
        <div className="card">
            <div className="card-content">
                <span className="card-title">{props.group.title}</span>
                <p>
                    {isPublic} | {members} | By <a href="#">{username}</a>
                </p>
            </div>

            <div className="card-action">
                <a href={`/groups/${props.group.uuid}/`}>Preview group</a>
            </div>
        </div>
    );
};

export default GroupCard;
