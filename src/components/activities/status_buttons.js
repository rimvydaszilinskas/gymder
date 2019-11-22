import React from 'react';

const StatusButtons = (props) => {
    // Display appropriate button for the user
    // If approve required is on and no request is given, show Request Join
    // If approve required is off and no request is given, show Join
    // If request is pending, show Pending
    // If request is approved, show Going
    // If request is denied, show Denied
    // Note that when the button is pressed the request is made or deleted automatically    
    const Button = () => {
        let value = 'Join';
        let disable = false;

        if (props.need_approval) {
            if (!props.request) {
                value = 'Request Join';
            } else if (props.request.status === 'approved') {
                value = 'Approved';
            } else if (props.request.status === 'pending') {
                value = 'Pending';
            } else {
                value = 'Declined';
                disable = true
            }
        } else {
            // Does not require approval
            if (props.request) {
                if (props.request.status === 'approved') {
                    value = 'Going';
                } else if (props.request.status === 'denied') {
                    value = 'Denied';
                    disable = true;
                }
            } 
        }

        return <button className="btn waves-effect" onClick={props.onClick} disabled={disable}>{value}</button>;
    };
    

    return (
        <div className="row center">
            <Button />
        </div>
    );
};

export default StatusButtons;
