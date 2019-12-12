import React from 'react';
import ReactDom from 'react-dom';

class UserGroups extends React.Component {
    constructor(props) {
        super(props);

        console.log(context);
    }

    render() {
        return (
            <React.Fragment>
            </React.Fragment>
        );
    }
}

ReactDom.render(
    <UserGroups />,
    document.getElementById('root')
);
