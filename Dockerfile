FROM phusion/baseimage:0.11

# Deactivate interactive configuration steps during package installation
ENV DEBIAN_FRONTEND noninteractive

# Upgrade Ubuntu for security patches
RUN apt-get update \
 && apt-get upgrade -y -o Dpkg::Options::="--force-confold" \
 # Install timezone info
 && apt-get install -y tzdata \
 # Setup timezone
 && cp /usr/share/zoneinfo/Europe/Berlin /etc/localtime \
 # Remove timezone info
 && apt-get remove -y tzdata \
 # Cleanup after APT
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Setup PIP
# RUN install_clean python3-pip python3-setuptools python3-wheel \
#  && python3 -m pip install --upgrade pip

# Install additional OS packages
RUN install_clean \
        mariadb-client

# Install application requirements
# COPY requirements.txt /app/requirements.txt
# RUN pip install --user -r /app/requirements.txt

# Install application files
COPY mysql_batch.py /app/mysql_batch.py
RUN touch /app/config.ini

# Set working directory
WORKDIR /app

# Setup image start
# ENTRYPOINT ["/sbin/my_init"]
ENTRYPOINT ["/usr/local/bin/python3", "/app/mysql_batch.py", "-c", "/app/config.ini", "/app/scripts"]

# Add labels to the image
LABEL org.label-schema.vcs-url="https://github.com/mastersign/mysql-batch"