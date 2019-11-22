import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';


class CreateActivity extends React.Component {
    constructor(props) {
        super(props);
        
        let today = new Date();

        this.state = {
            user: context.user,
            form: {
                title: `${context.user.username} activity`,
                description: '',
                time: (today.getHours() < 10 ? '0' : '') + today.getHours() + ':' + (today.getMinutes() < 10 ? '0': '') + today.getMinutes(),
                date: today.getFullYear() + '-' + (today.getMonth() < 10 ? '0' : '') + today.getMonth() + '-' + (today.getDate() + 7 < 10 ? '0' : '') + today.getDate(),
                address: '',
                needs_approval: false,
                public: true,
                max_attendees: 5,
                price: 0,
                duration: 60
            },
            group_activity: false,
            address_validated: false,
            address_uuid: null,
            errors: null
        };

        this.handleLabelInput = this.handleLabelInput.bind(this);
        this.handleDescriptionInput = this.handleDescriptionInput.bind(this);
        this.handleDateInput = this.handleDateInput.bind(this);
        this.handleTimeInput = this.handleTimeInput.bind(this);
        this.handleAddressInput = this.handleAddressInput.bind(this);
        this.handleAddressValidation = this.handleAddressValidation.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
        this.handleApprovalInput = this.handleApprovalInput.bind(this);
        this.handlePublicInput = this.handlePublicInput.bind(this);
        this.handleGroupInput = this.handleGroupInput.bind(this);
        this.handleAttendeeInput = this.handleAttendeeInput.bind(this);
        this.handlePriceInput = this.handlePriceInput.bind(this);
        this.handleDurationInput = this.handleDurationInput.bind(this);
    }

    handleLabelInput(e) {
        let form = this.state.form;

        form.title = e.target.value;

        this.setState({
            form: form
        });
    }

    handleDescriptionInput(e) {
        let form = this.state.form;
        form.description = e.target.value;
        this.setState({
            form: form
        });
    }

    handleDateInput(e) {
        let form = this.state.form;
        form.date = e.target.value;
        this.setState({
            form: form
        });
    }

    handleTimeInput(e) {
        let form = this.state.form;
        form.time = e.target.value;
        this.setState({
            form: form
        });
    }

    handleAddressInput(e) {
        let form = this.state.form;
        form.address = e.target.value;
        this.setState({
            // address_validated: false,
            form: form
        });
    }

    handleDurationInput(e) {
        let value = parseInt(e.target.value);

        if (value > 600) {
            return;
        }

        let form = this.state.form;
        form.duration = e.target.value;
        this.setState({
            form: form
        });
    }

    handleAddressValidation(e) {
        // lookup valid addresses and then cycle through them for the user to confirm
        // if the address is confirmed by the user, the human representation is added to the form and
        // the uuid is added to be sent to the server
        e.preventDefault();

        if (this.state.address_validated) {
            alert('Address already validated');
            return;
        }

        fetch('/api/utils/addresses/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                address: this.state.form.address
            })
        }).then(response => {
            if(response.status === 200) {
                response.json().then(responseJSON => {
                    if (Array.isArray(responseJSON)){
                        if(responseJSON.length === 0) {
                            alert('Cannot find address')
                            return;
                        }

                        responseJSON.some(resp => {
                            let answer = confirm(`Is the address correct: ${resp.address}?`);
                            if (answer) {
                                // if user selects this address add the uuid as the correct choice
                                let form = this.state.form;

                                form.address = resp.address;

                                this.setState({
                                    address_uuid: resp.uuid,
                                    address_validated: true,
                                    form: form
                                });
                                return true;
                            }
                        });
                    } else {
                        throw Error('Not an array')
                    }
                });
            } else {
                alert('Something went wrong... Try again!')
            }
        }).catch(e => {
            alert('An error has occured!');
            console.log(e);
        });
    }

    handleFormSubmit(e) {
        // this is the final method for the view
        // only execute this if the address is verified with the backend
        // check to see if all the values are not null
        e.preventDefault();

        // decide on the url based on group/individual activity
        let url = this.state.group_activity ? '/api/activities/group/' : '/api/activities/individual/';
        
        // pull out form from the state to modify it before request
        // use spread operator to copy the object
        let form = {...this.state.form};

        // attach address uuid
        form.address_uuid = this.state.address_uuid;
        
        // change the date and time format to datetime
        let date = form.date;
        let time = form.time;
        let datetime = `${date}T${time}:00Z`;
                
        delete form.address;
        delete form.date;

        form.time = datetime;

        fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify(form)
        }).then(response => {
            if (response.ok) {
                response.json().then(responseJSON => {
                    window.location.replace(`/activities/${responseJSON.uuid}/?created=true`);
                }).catch(e => {
                });
            } else {
                alert('There were errors');
            }
        }).catch(e => {
            console.log(e);
            alert('Something went really wrong!')
        });        
    }

    handleApprovalInput() {
        let form = this.state.form;
        form.needs_approval = !form.needs_approval;
        this.setState({
            form: form
        });
    }

    handlePublicInput() {
        let form = this.state.form;
        form.public = !form.public;
        this.setState({
            form: form
        });
    }

    handleGroupInput() {
        this.setState({
            group_activity: !this.state.group_activity
        });
    }

    handleAttendeeInput(e) {
        let form = this.state.form;
        form.max_attendees = e.target.value;
        this.setState({
            form: form
        });
    }

    handlePriceInput(e) {
        let form = this.state.form;
        let value = parseFloat(e.target.value)

        if (value > 100) {
            alert('Price cannot exceed 100!');
            return;
        }

        form.price = e.target.value;
        this.setState({
            form: form
        });
    }

    render() {
        return (
            <React.Fragment>
                <div className="row">
                    <div className="row center">
                        <h3>Create activity</h3>
                    </div>

                    <div className="row card-panel">
                        <div className="row">
                            <div className="col m2 hide-on-small-only"></div>
                            <div className="col m8 s12">
                                <form ref="form" onSubmit={this.handleFormSubmit}>
                                    <div className="row">
                                        <div className="input-field">
                                            <input type="text" className="validate center" id="title" value={this.state.form.title} onChange={this.handleLabelInput} required></input>
                                            <label htmlFor="title">Activity name</label>
                                        </div>
                                    </div>

                                    <div className="row">
                                        <div className="input-field">
                                            <textarea id="description" value={this.state.form.description} onChange={this.handleDescriptionInput} className="materialize-textarea"></textarea>
                                            <label htmlFor="description">Description</label>
                                        </div>
                                    </div>

                                    <h5>Activity logistics</h5>

                                    <div className="row">
                                        <div className="col m4 input-field">
                                            <input type="date" id="date" className="center datepicker" value={this.state.form.date} onChange={this.handleDateInput} required></input>
                                            <label htmlFor="date">Date</label>
                                        </div>
                                        <div className="col s4 input-field">
                                            <input type="time" id="time" className="center timepicker" value={this.state.form.time} onChange={this.handleTimeInput} required></input>
                                            <label htmlFor="time">Time</label>
                                        </div>
                                        <div className="col s4 input-field">
                                            <input type="number" id="duration" className="center" min="5" max="600" value={this.state.form.duration} onChange={this.handleDurationInput} required></input>
                                            <label htmlFor="duration">Duration</label>
                                            <span className="helper-text" data-error="wrong" data-success="right">
                                                Duration is in minutes
                                            </span>
                                        </div>
                                    </div>

                                    <div className="row">
                                        <div className="col m6 input-field">
                                            <center>
                                                <label>
                                                    <input type="checkbox" id="needs_approval" checked={this.state.form.needs_approval ? 'checked': ''} onChange={this.handleApprovalInput}/>
                                                    <span>Needs approval</span>
                                                    <span className="helper-text" data-error="wrong" data-success="right">
                                                        {this.state.form.needs_approval ? 'You will have to approve requesting users' : 'Users can join freely'}
                                                    </span>
                                                </label>
                                            </center>
                                        </div>

                                        <div className="col m6 input-field">
                                            <center>
                                                <label>
                                                    <input type="checkbox" id="public" checked={this.state.form.public ? 'checked' : ''} onChange={this.handlePublicInput}></input>
                                                    <span>Public</span>
                                                    <span className="helper-text" data-error="wrong" data-success="right">
                                                        {this.state.form.public ? 'Activity is public for anyone to join' : 'Activity requires invitations'}
                                                    </span>
                                                </label>
                                            </center>
                                        </div>

                                        <div className="row">
                                            <div className="col m6 input-field">
                                                <center>
                                                    <label>
                                                        <input type="checkbox" id="group_activity" checked={this.state.group_activity ? 'checked' : ''} onChange={this.handleGroupInput}></input>
                                                        <span>Group activity</span>
                                                        <span className="helper-text" data-error="wrong" data-success="right">
                                                            {this.state.group_activity ? 'Activity can be joined by more than one attendee' : 'Activity can be joined by maximum 1 attendee'}
                                                        </span>
                                                    </label>
                                                </center>
                                            </div>
                                            <div className="col m6 input-field">
                                                <input className="validate" type="number" min="3" max="20" value={this.state.form.max_attendees} onChange={this.handleAttendeeInput} disabled={!this.state.group_activity}></input>
                                            </div>
                                        </div>

                                        { this.state.group_activity ? 
                                            <div className="row">
                                                <div className="col s12 input-field">
                                                    <input type='number' min='0' max='100' step=".01" id="value" value={this.state.form.price} onChange={this.handlePriceInput}></input>
                                                    <label htmlFor="price">Price</label>
                                                    <span className="helper-text" data-error="wrong" data-success="right">
                                                        Leave price as "0" to make it free
                                                    </span>
                                                </div>
                                            </div> : <React.Fragment></React.Fragment>}
                                    </div>

                                    <div className="row">
                                        <div className="col s10 input-field">
                                            <input type="text" className="validate" id="address" value={this.state.form.address} onChange={this.handleAddressInput} required></input>
                                            <label htmlFor="address">Address</label>
                                        </div>
                                        <div className="col s2">
                                            <button className="btn" onClick={this.handleAddressValidation}>Verify</button>
                                        </div>
                                    </div>

                                    <div className="row center">
                                        <button className="btn" type="submit" disabled={!this.state.address_validated}>Continue</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </React.Fragment>
        );
    }
}


ReactDom.render(
    <CreateActivity />,
    document.getElementById('root')
);
