import React from 'react';
import ReactDom from 'react-dom';

class Index extends React.Component {
    render() {
        return (
            <h1>Hello world!</h1>
        );
    }
}

ReactDom.render(
    <Index />,
    document.getElementById('root')
);