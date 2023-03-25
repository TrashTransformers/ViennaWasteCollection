import { DefaultService as ClassifyService } from './core/api/classify'
import { Component, EventEmitter, Output } from "@angular/core";

@Component({
    selector: 'file-upload',
    templateUrl: "file-upload.component.html",
    styleUrls: ["file-upload.component.scss"]
})
export class FileUploadComponent {

    fileName = '';

    imageURL = '';

    @Output() classification = new EventEmitter<Classification>();

    constructor(private classifyService: ClassifyService) { }

    onFileSelected(event: any) {

        const file: File = event.target.files[0];

        if (file) {

            this.fileName = file.name;
            const reader = new FileReader();
            reader.onload = () => {
                this.imageURL = reader.result as string;
            }
            reader.readAsDataURL(file)

            this.classifyService.createFileClassifyPost(file).subscribe((result: Classification) => {
                this.classification.emit(result);
            });
        }
    }
}

export interface Classification {
    category: string;
    confidence: number;
}