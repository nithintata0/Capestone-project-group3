import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { Router } from '@angular/router';
import firebase from 'firebase/app';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(public auth: AngularFireAuth,
    private router:Router
    ) { }

  ngOnInit(): void {
    
  }

  googleSignIN(){
    this.auth.signInWithPopup(new firebase.auth.GoogleAuthProvider()).then(
      (data)=>{
        console.log(data.user)
        if(data.user){

          this.router.navigate(['jobs'])

        }
      }
    );
  }
}
