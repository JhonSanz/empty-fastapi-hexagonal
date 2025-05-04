docker build -f generator.dockerfile -t hexagon-generator .
docker run -p 8069:8069 -v "${PWD}:/mounted_project" hexagon-generator