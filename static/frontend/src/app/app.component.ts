import {Component} from '@angular/core';
import {TrackService} from './track.service';
import {Observable} from 'rxjs/Rx';

@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.css']
})
export class AppComponent {

	/**
	 * An array of all the Track objects from the API
	 */
	public Tracks;

	/**
	 * An object representing the data in the "add" form
	 */
	public new_Track: any;

	public fields: any;

	public validationFields: any;

	public data: any;

	public files: any;

	public fileData: any;

	public userData: any;

	constructor(private _TrackService : TrackService) { }

	ngOnInit() {
		this.fields = {};
		this.new_Track = this.getTrackObject();
		this.validationFields = ["host", "username", "password"];
	}

	setFiles(event) {
		this.files = [];
		for(var i = 0; i < event.srcElement.files.length; i++) {
			this.files.push(event.srcElement.files[i]);
		}
	}

	uploadFile() {
		if(this.files.length > 0) {
			this._TrackService.uploadFile(this.files).subscribe(
				data => {
					let res: any;
					res = data;
					if(res.message) {
						alert(res.message);
					}
					this.fileData = res.data;
					return true;
				},
				error => {
					console.error("Error saving!");
					return Observable.throw(error);
				}
			);
		}
	}

	getTrackObject() {
		var obj = {
			"host": "",
			"username": "",
			"password": "",
			"port": ""
		}
		return obj;
	}

	clearFields() {
		this.fields = {};
		this.new_Track = this.getTrackObject();
	}

	isEmptyField(value) {
		return value == "" || value == null || value == undefined;
	}

	isValidForm() {
		this.validationFields.forEach(field => {
			this.fields[field] = {required: this.isEmptyField(this.new_Track[field])}
		});
		let isValid = true;
		this.validationFields.forEach(field => {
			if(this.fields[field].required) {
				isValid = false;
				return;
			} 
		});
		return isValid;
	}

	connectServer() {
		if(this.isValidForm()) {
			this._TrackService.connect(this.new_Track).subscribe(
				data => {
					let res: any;
					res = data;
					if(res.message) {
						alert(res.message);
					}
					this.userData = res.data;
					// this.getTracks();
					return true;
				},
				error => {
					console.error("Error saving!");
					return Observable.throw(error);
				}
			);
		}
	}
}
