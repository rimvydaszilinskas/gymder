import React from 'react';
import ReactDom from 'react-dom';
import getCookie from '../utils/get_cookie';

class CreateGroup extends React.Component {
    constructor(props) {
        super(props);
        
        this.state = {
            user: context.user,
            group: {
                title: '',
                description: '',
                public: true,
                needs_approval: false
            }
        };

        this.handleTitleInput = this.handleTitleInput.bind(this);
        this.handleDescriptionInput = this.handleDescriptionInput.bind(this);
        this.handlePublicInput = this.handlePublicInput.bind(this);
        this.handleNeedApprovalInput = this.handleNeedApprovalInput.bind(this);
        this.formSubmit = this.formSubmit.bind(this);
    }

    handleTitleInput(e) {
        let group = this.state.group;

        group.title = e.target.value
        
        this.setState({
            group: group
        });
    }

    handleDescriptionInput(e) {
        let group = this.state.group;

        group.description = e.target.value;

        this.setState({
            group: group
        });
    }

    handlePublicInput() {
        let group = this.state.group;

        group.public = !group.public;

        this.setState({
            group: group
        });
    }

    handleNeedApprovalInput() {
        let group = this.state.group;

        group.needs_approval = !group.needs_approval;

        this.setState({
            group: group
        });
    }

    formSubmit(e) {
        e.preventDefault();
        
        fetch('/api/groups/', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(this.state.group)
        }).then(response => {
            if(response.status === 201) {
                response.json().then(json => {
                    window.location.assign(`/groups/${json.uuid}`);
                });
            } else {
                alert('Something went wrong');
            }
        }).catch(error => {
            console.log(error);
            alert('Something went wrong');
        });
    }

    render() {
        return (
            <div className="container">
                <div className="row">
                    <center>
                        <h3>Create Group</h3>
                    </center>
                </div>

                <div className="row card-panel">
                    <div className="col s2 hide-on-small-only"></div>
                    <div className="col m8 s12">
                        <form ref="form" onSubmit={this.formSubmit}>
                            <div className="row">
                                <div className="input-field">
                                    <input type="text" className="validate center" id="title" value={this.state.group.title} onChange={this.handleTitleInput} required></input>
                                    <label htmlFor="title">Title</label>
                                </div>
                            </div>

                            <div className="row">
                                <div className="input-field">
                                    <textarea id="description" className="materialize-textarea" value={this.state.group.description} onChange={this.handleDescriptionInput}></textarea>
                                    <label htmlFor="description">Description</label>
                                </div>
                            </div>

                            <div className="row">
                                <div className="col m6 input-field">
                                    <center>
                                        <label>
                                            <input type="checkbox" id="public" checked={this.state.group.public ? 'checked': ''} onChange={this.handlePublicInput}></input>
                                            <span>Public</span>
                                            <span className="helper-text" data-error="wrong" data-success="right">
                                                {this.state.group.public ? 'Group is public for anyone to see': 'Group will require invitations to be visible'}
                                            </span>
                                        </label>
                                    </center>
                                </div>
                                <div className="col m6 input-field">
                                    <center>
                                        <label>
                                            <input type="checkbox" id="needs-approval" checked={this.state.group.needs_approval ? 'checked': ''} onChange={this.handleNeedApprovalInput}></input>
                                            <span>Needs approval</span>
                                            <span className="helper-text" data-error="wrong" data-success="right">
                                                {this.state.group.needs_approval ? 'Anyone who can see the group can join': 'Users will have to be approved'}
                                            </span>
                                        </label>
                                    </center>
                                </div>
                            </div>

                            <div className="row center">
                                <button className="btn" type="submit" disabled={this.state.group.title.length < 3}>Create</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

ReactDom.render(
    <CreateGroup />,
    document.getElementById('root')
);
