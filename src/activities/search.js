import React from 'react';
import ReactDom from 'react-dom';
import ActivityCard from '../components/activities/activity_card';
import getCookie from '../utils/get_cookie';

class SearchActivities extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            searchQuery: '',
            activities: [],
            received: false
        };

        this.handleSearchEntry = this.handleSearchEntry.bind(this);
        this.handleSearchSubmit = this.handleSearchSubmit.bind(this);
    }

    handleSearchEntry(e) {
        this.setState({
            searchQuery: e.target.value
        });
    }

    handleSearchSubmit(e) {
        this.setState({
            received: false
        });

        fetch(`/api/activities/?query=${this.state.searchQuery}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
        }).then(response => {
            response.json().then(json => {
                this.setState({
                    activities: json,
                    received: true
                });
            });
        }).catch(err => {
            console.log(err);
            alert('Error while searching');
        });
    }

    render() {
        return (
            <div className="container margin-top">
                <div className="row">
                    <div className="input-field col s10">
                        <i className="material-icons prefix">search</i>
                        <input type="text" id="search" value={this.state.searchQuery} onChange={this.handleSearchEntry}></input>
                        <label htmlFor="search">Search</label>
                    </div>
                    <div className="col s2">
                        <button className="btn margin-top" onClick={this.handleSearchSubmit}>Search</button>
                    </div>
                </div>

                <div className="row">
                    {
                        this.state.activities.length === 0 && this.state.received ?
                            <center>No results</center> 
                            : this.state.activities.map((activity, index) => {
                                return (<ActivityCard activity={activity} key={index}/>);
                            })
                    }
                </div>

                <div className="row">
                    <span className="help-text">{this.state.activities.length} search results</span>
                </div>
            </div>
        );
    }
}

ReactDom.render(
    <SearchActivities />,
    document.getElementById('root')
);
