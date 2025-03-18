import axios from "axios";
const UploadOMR = () => {
    const handleUpload = async (event) => {
        const formData = new FormData();
        formData.append("omrSheet", event.target.files[0]);
        formData.append("examType", "JEE");

        const response = await axios.post("http://localhost:5000/api/exams/process-omr", formData);
        console.log(response.data);
    };

    return <input type="file" onChange={handleUpload} />;
};
export default UploadOMR;
