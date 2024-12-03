

# 🌾 RV_Diagnoze: Revolutionizing Rice Crop Health Management

Welcome to **RV_Diagnoze**, an AI-powered web application designed to empower farmers, agronomists, and researchers in their quest to maintain healthy rice crops. With advanced image-based disease classification, intuitive UI, and responsive design, RV_Diagnoze is your ultimate companion in ensuring the well-being of your rice fields. Dive into the world of precision agriculture with this innovative tool that makes crop health management both effective and effortless.

## 🚀 Why RV_Diagnoze?

In the world of agriculture, time is of the essence. Diseases can spread rapidly, devastating crops and leading to significant losses. RV_Diagnoze offers a quick, reliable solution to identify and manage rice crop diseases, leveraging cutting-edge AI technology to deliver accurate diagnoses and actionable insights right at your fingertips.

## 🎯 Key Features

### 🌟 **Advanced Image-Based Classification**
- **State-of-the-Art Deep Learning Model**: Our application employs a finely-tuned Convolutional Neural Network (CNN) model, meticulously trained on a robust dataset of rice leaf images to ensure accurate and reliable disease classification.
- **10 Disease Categories**: RV_Diagnoze can accurately classify images into one of the following categories:
  - **Bacterial Leaf Blight**
  - **Brown Spot**
  - **Healthy**
  - **Leaf Blast**
  - **Leaf Scald**
  - **Narrow Brown Spot**
  - **Neck Blast**
  - **Rice Hispa**
  - **Sheath Blight**
  - **Tungro**

### 🛠️ **Tailored Remedies and Care Instructions**
- **Custom Remedy Suggestions**: For each identified disease, the tool provides specific, actionable remedies to manage and mitigate the issue.
- **Fertilizer Recommendations**: Get tailored advice on the best fertilizers to strengthen your plants against diseases.
- **Pesticide Options**: Access recommendations on effective pesticides to combat pests and diseases, ensuring your crops stay healthy.

### 📱 **Responsive and Engaging UI/UX**
- **Dynamic and Intuitive Interface**: Designed with a user-first approach, the UI adapts seamlessly to different devices, offering a smooth and engaging experience whether on desktop or mobile.
- **Enhanced Animations**: Delight in a visually appealing interface with smooth animations that make user interaction both intuitive and enjoyable.

### 📊 **Comprehensive Logging and Reporting**
- **Detailed Prediction Logs**: Each diagnosis is logged with essential details like timestamp, filename, predicted label, and confidence score, providing a thorough record of your crop health management. The logs are stored in an SQLite database, ensuring secure and reliable storage.
- **Database Support**: The logs are managed through an SQLite database, making it easy to track and analyze your crop’s health over time.

### 📲 **Seamless WhatsApp Integration**
- **Diagnosis Report Sharing**: After receiving a diagnosis, RV_Diagnoze can send the details of the diagnosis when "Send Details via Whatsapp" button is clicked, including remedies and recommendations, to the phone number associated with your account via WhatsApp. This ensures that you have quick access to the information, even when you're on the go.

## 🛠️ Installation & Setup

Ready to get started? Follow these steps to set up RV_Diagnoze on your local machine:

### 1. **Clone the Repository**
   Start by cloning the RV_Diagnoze repository:
   ```bash
   git clone https://github.com/yourusername/RV_Diagnoze.git
   cd RV_Diagnoze
   ```

### 2. **Place the Dataset**
   Download the [Rice Disease Varieties Dataset](https://www.kaggle.com/datasets/jerostanley/rice-disease-varieties/data) and place it inside the `dataset/` directory within the `RV_Diagnoze` folder. This ensures that all the necessary data is readily accessible for the application.

   Your directory structure should now include:
   ```plaintext
   RV_Diagnoze/
   ├── dataset/
   │   ├── Bacterial_Leaf_Blight/
   │   ├── Brown_Spot/
   │   ├── Healthy/
   │   ├── ...
   ```

### 3. **Install Dependencies**
   Ensure Python is installed on your system. Then, install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

### 4. **Train the Model**
   Before using the application, you need to train the model. Open the `Model_Training.ipynb` Jupyter Notebook and follow the instructions to train the model using the dataset. Once the training is complete, the trained model will be saved as `model.h5` in the `RV_Diagnoze/` directory.

   *Note: The application will not function until the model is trained and the `model.h5` file is generated.*

### 5. **Download and Place Video Files**
   You will need to download videos related to each rice disease. These videos can be sourced from platforms like YouTube or other educational resources, based on your preferences. Once downloaded, the videos should be placed in the `static/videos/` directory within the `RV_Diagnoze/` folder. Ensure that each video is named according to the corresponding disease as listed below:

   - `bacterial_leaf_blight.mp4` - Video for Bacterial Leaf Blight
   - `brown_spot.mp4` - Video for Brown Spot
   - `healthy.mp4` - Video for Healthy leaves
   - `leaf_blast.mp4` - Video for Leaf Blast
   - `leaf_scald.mp4` - Video for Leaf Scald
   - `narrow_brown_spot.mp4` - Video for Narrow Brown Spot
   - `neck_blast.mp4` - Video for Neck Blast
   - `rice_hispa.mp4` - Video for Rice Hispa
   - `sheath_blight.mp4` - Video for Sheath Blight
   - `tungro.mp4` - Video for Tungro

   This ensures that the correct video is played for each diagnosis.

### 6. **Run the Flask Application**
   After the model is trained and videos are placed correctly, launch the application by executing:
   ```bash
   python app.py
   ```
   Visit `http://127.0.0.1:8080/` in your browser to start using the tool.

*Note: The trained model and video files will be stored in the `RV_Diagnoze/` directory, making it easy to manage and deploy along with the application.*

## 🧠 Model Training and Architecture

### **Dataset**
The model at the heart of RV_Diagnoze was trained on a carefully curated dataset of rice leaf images, which you can access on Kaggle. This dataset includes thousands of images from various rice fields, meticulously labeled by agricultural experts to ensure high accuracy.

### **Model Architecture**
- **Convolutional Neural Network (CNN)**: The model is built on a CNN architecture, featuring multiple layers of convolutional filters, pooling, and fully connected layers. This architecture was fine-tuned to achieve the highest possible accuracy in classifying rice leaf diseases.
- **Preprocessing**: Images are preprocessed by resizing to a consistent size, normalizing pixel values, and augmenting the dataset to enhance the model's generalization capabilities.

### **Training Process**
- The model was trained using the TensorFlow framework, with extensive hyperparameter tuning performed to optimize performance. Training was carried out on a GPU to expedite the process and improve model efficiency.

### **Evaluation Metrics**
- The model’s effectiveness was evaluated using metrics such as accuracy, precision, recall, and F1-score, ensuring it meets the demands of real-world agricultural applications.

## 📂 Project Structure

Here’s an overview of the directory structure for the RV_Diagnoze project:

```plaintext
RV_Diagnoze/
├── app.py                # Main Flask application and route definitions
├── Model_Training.ipynb  # Jupyter Notebook for training the CNN model
├── requirements.txt      # List of dependencies required for the project
├── static/               # Static assets such as CSS, images, and videos
│   ├── css/              # Stylesheets for the application
│   ├── uploads/          # Directory where uploaded images are stored
│   └── videos/           # Video files related to each disease
│       ├── bacterial_leaf_blight.mp4   # Video for Bacterial Leaf Blight
│       ├── brown_spot.mp4              # Video for Brown Spot
│       ├── healthy.mp4                 # Video for Healthy leaves
│       ├── leaf_blast.mp4              # Video for Leaf Blast
│       ├── leaf_scald.mp4              # Video for Leaf Scald
│       ├── narrow_brown_spot.mp4       # Video for Narrow Brown Spot
│       ├── neck_blast.mp4              # Video for Neck Blast
│       ├── rice_hispa.mp4              # Video for Rice Hispa
│       ├── sheath_blight.mp4           # Video for Sheath Blight
│       └── tungro.mp4                  # Video for Tungro
├── templates/            # HTML templates for rendering the web pages
│   ├── index.html        # Main page with file upload and result display
│   ├── login.html        # Login page for user authentication
│   ├── signup.html       # Signup page for new users
│   ├── get_started.html  # Landing page introducing the tool
│   └── disease_templates/ # HTML files for each disease (e.g., bacterial_leaf_blight.html)
├── flask_app.db          # SQLite database for storing user and prediction logs
├── dataset/              # Directory to store the rice disease dataset
│   ├── Bacterial_Leaf_Blight/  # Subdirectory for Bacterial Leaf Blight images
│   ├── Brown_Spot/             # Subdirectory for Brown Spot images
│   ├── Healthy/                # Subdirectory for Healthy images
│   ├── Leaf_Blast/             # Subdirectory for Leaf Blast images
│   ├── Leaf_Scald/             # Subdirectory for Leaf Scald images
│   ├── Narrow_Brown_Spot/      # Subdirectory for Narrow Brown Spot images
│   ├── Neck_Blast/             # Subdirectory for Neck Blast images
│   ├── Rice_Hispa/             # Subdirectory for Rice Hispa images
│   ├── Sheath_Blight/          # Subdirectory for Sheath Blight images
│   └── Tungro/                 # Subdirectory for Tungro images
├── model.h5              # Trained model file for classification
└── README.md             # This file - documentation for the project
```

## ✨ How to Use RV_Diagnoze

Once you have the RV_Diagnoze application up and running, here’s how you and others can use the tool:

### 1. **Access the Application**
   Open your browser and navigate to `http://127.0.0.1:8080/` (or the appropriate IP address/hostname if deployed on a server). You will be greeted with the homepage where you can get started.

### 2. **Sign Up / Log In**
   - **New Users**: Click on the **Sign Up** button to create a new account. Fill in your details and click **Submit**. Once your account is created, you’ll be redirected to the login page.
   - **Returning Users**: Enter your credentials on the **Login** page to access the main features of RV_Diagnoze.

### 3. **Upload an Image for Diagnosis**
   - After logging in, you’ll be directed to the main page where you can upload an image of a rice leaf. Click the **Choose File** button, select your image, and click **Detect**.
   - The tool will process the image and provide a diagnosis, displaying the identified disease (if any), along with tailored remedies, fertilizer recommendations, and pesticide options.

### 4. **View Detailed Information**
   - For more details on the diagnosis, click on the **Know More** button. This will provide a deeper dive into the identified disease, including additional resources and information.

### 5. **Receive WhatsApp Notifications**
   - The diagnosis results will be automatically sent to the phone number associated with your account via WhatsApp when the "Send Results via WhatsApp" button is clicked. This ensures that you have quick access to the information even when you're away from your computer.

### 6. **Explore Disease-Specific Information**
   - Use the navigation menu to explore detailed information about specific diseases. Each disease has a dedicated page with a description, remedies, fertilizer, and pesticide recommendations, as well as related videos.

## 🎨 UI/UX Design Highlights

- **Hero Section**: Greeted by a captivating hero section that introduces the tool with a welcoming message and a 'Learn More' button, which smoothly scrolls to the 'About Our Tool' section.
- **Navigation Bar**: A sticky navigation bar that remains visible as you scroll, ensuring easy access to different sections. For mobile views, the navbar transitions to a hamburger menu, maintaining usability across all devices.
- **Information-Rich Sections**: Detailed content is spread across 14 to 15 sections, providing in-depth information about the tool, disease descriptions, remedies, and more.
- **Scroll-Triggered Animations**: Engaging animations that activate as you scroll, adding a dynamic touch to the user experience.

## 🤝 Contributions & Acknowledgements

We believe in the power of community and collaboration. If you have ideas for improving RV_Diagnoze or wish to contribute new features, feel free to fork the repository, make your changes, and submit a pull request. We welcome contributions that help make this tool better for everyone.

### Acknowledgements
- **Contributors**: A special thank you to everyone who contributed to the development of this tool, from ideation to deployment.
- **Dataset Providers**: Our gratitude goes out to the creators of the [Rice Disease Varieties Dataset](https://www.kaggle.com/datasets/jerostanley/rice-disease-varieties/data) on Kaggle, whose work made this project possible.

## 📧 Contact Information

For any inquiries, feedback, or support, please reach out to Jerophin D R at **[jerophinstanley47@gmail.com]**. We look forward to hearing from you and working together to improve RV_Diagnoze!

