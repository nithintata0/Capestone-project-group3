import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore } from '@angular/fire/firestore';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import * as ClassicEditor from '@ckeditor/ckeditor5-build-classic';

@Component({
  selector: 'app-add-job',
  templateUrl: './add-job.component.html',
  styleUrls: ['./add-job.component.scss']
})
export class AddJobComponent implements OnInit {
  public Editor = ClassicEditor;
  validateForm!: FormGroup;
  docId: any

  constructor(private fb: FormBuilder, private afs: AngularFirestore, private route: ActivatedRoute, private auth: AngularFireAuth, private router: Router,) { }

  ngOnInit(): void {


    this.validateForm = this.fb.group({
      loation: [null, [Validators.required]],
      jobType: [null, [Validators.required]],
      jobDesc: [null, [Validators.required]],
      jobTitle: [null, [Validators.required]]
    });
    this.route.queryParams.subscribe(
      (params) => {
        console.log(params)
        if (params['id']) {
          this.docId = params['id']
          this.afs.collection('jobs').doc(this.docId).get().subscribe(
            (data) => {
              console.log(data.data())
              if (data.data()['jobTitle']) {
                this.validateForm.setValue(data.data())
              } else {
                let formData = data.data()
                formData['jobTitle'] = ""
                this.validateForm.setValue(formData)
              }

            }
          )
        }

      });
    this.getUserDetails()
  }
  getUserDetails() {

    this.auth.authState

      .subscribe(
        (user) => {
          console.log(user)

          if (user) {
            // this.userName = user.displayName

            const admins = ['thumusreerukmini9@gmail.com', 'ramkiransampathi@gmail.com', 'saicharitha905@gmail.com', 'tatanithin007@gmail.com', 'jaswanthtata@gmail.com']
            const userEmail = user.email
            console.log(admins.includes(userEmail))
            if (admins.includes(userEmail)) {

            } else {
              this.router.navigate(['jobs'])
            }

          } else {
            this.router.navigate(['home'])
          }


        }
      )
  }
  submitForm() {
    for (const i in this.validateForm.controls) {
      this.validateForm.controls[i].markAsDirty();
      this.validateForm.controls[i].updateValueAndValidity();
    }
    if (this.validateForm.valid) {
      console.log(this.validateForm.value)
      if(this.docId){
        this.afs.collection('jobs').doc(this.docId).set(
          this.validateForm.value
        ).then(
          (doc)=>{
            this.router.navigate(['admin'])
          }
        )
      }else{

      
      this.afs.collection('jobs').add(this.validateForm.value).then(
        (data) => {
          this.validateForm.reset()
        }
      )
    }
    }
  }

}
