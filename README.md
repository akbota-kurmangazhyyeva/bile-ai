# DanceGen Backend

DanceGen is an innovative application that generates dance movements based on user-provided music. This repository contains the backend service built with FastAPI, which processes audio files and generates corresponding dance animations using the EDGE (Editable Dance Generation) model.

## Features

- Process uploaded audio files
- Generate dance animations using the EDGE model
- Upload generated animations to Amazon S3
- RESTful API for easy integration with frontend applications

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.9 or higher
- Docker (for containerized deployment)
- An Amazon S3 bucket for storing generated animations

## Installation

To set up the DanceGen backend locally, follow these steps:

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/dancegen-backend.git
   cd dancegen-backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_BUCKET_NAME=your_s3_bucket_name
   ```

## Usage

To run the backend service locally:

1. Ensure you're in the project root directory and your virtual environment is activated.

2. Start the FastAPI server:
   ```
   uvicorn app.main:app --reload
   ```

3. The API will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- `POST /api/v1/process-music/`: Upload an audio file to generate a dance animation.

For detailed API documentation, refer to the Swagger UI available at `/docs` when the server is running.

## Docker Deployment

To deploy the backend using Docker:

1. Build the Docker image:
   ```
   docker build -t dancegen-backend .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 --env-file .env dancegen-backend
   ```

The API will be available at `http://localhost:8000`.

## Contributing

Contributions to the DanceGen backend are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [creating a pull request](https://help.github.com/articles/creating-a-pull-request/).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please contact the project maintainers at [your-email@example.com](mailto:your-email@example.com).
