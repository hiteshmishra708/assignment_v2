import {Injectable} from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie';

@Injectable()
export class TrackService {

    // http options used for making any writing API calls
    private httpOptions: any;

    constructor(private http:HttpClient, private _cookieService:CookieService) {
        // CSRF token is needed to make API calls work when logged in
        let csrf = this._cookieService.get("csrftoken");
        // the Angular HttpHeaders class throws an exception if any of the values are undefined
        if (typeof(csrf) === 'undefined') {
          csrf = '';
        }
        this.httpOptions = {
          headers: new HttpHeaders({ 'Content-Type': 'application/json', 'X-CSRFToken': csrf })
        };
    }

    // NOTE: all API calls in this file use simple endpoints served by
    // an Express app in the file app.js in the repo root. See that file
    // for all back-end code.

    // Uses http.get() to load data from a single API endpoint
    list() {
        return this.http.get('tracks/');
    }

    // send a POST request to the API to upload files
    uploadFile(files) {
        var formData = new FormData();
        for (var i in files) {
            formData.append("myFile", files[i], files[i].name)
        }
        return this.http.post('extract/', formData);
    }
    
    // send a POST request to the API to connect to the linux server
    connect(track) {
        let body = JSON.stringify(track);
        return this.http.post('connect/', body, this.httpOptions);
    }
}
