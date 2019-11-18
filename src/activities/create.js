import React from 'react';
import ReactDom from 'react-dom';


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
                price: 0
            },
            group_activity: false,
            address_validated: true
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
            form: form
        });
    }

    handleAddressValidation(e) {
        e.preventDefault();

    }

    handleFormSubmit(e) {
        e.preventDefault();

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
                                <form ref="form" onSubmit={()=>{}}>
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
                                        <div className="col m6 input-field">
                                            <input type="date" className="center datepicker" value={this.state.form.date} onChange={this.handleDateInput} required></input>
                                            <label htmlFor="date">Date</label>
                                        </div>
                                        <div className="col s6 input-field">
                                            <input type="time" className="center timepicker" value={this.state.form.time} onChange={this.handleTimeInput} required></input>
                                            <label htmlFor="time">Time</label>
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
                                        <button className="btn" onClick={this.handleFormSubmit} disabled={!this.state.address_validated}>Continue</button>
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
