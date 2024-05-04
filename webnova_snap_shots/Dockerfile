FROM ubuntu:focal
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && \
    apt-get install -y vim python3-dev python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN useradd -ms /bin/bash eddiechang091 && \
    mkdir -p /home/eddiechang091/mission_config /home/eddiechang091/entry_point \
             /home/eddiechang091/input_queue /home/eddiechang091/output_queue
WORKDIR /home/eddiechang091/entry_point
COPY run_executable.sh executable.py /home/eddiechang091/entry_point/
RUN chmod +x run_executable.sh
COPY mission_config1714441180613.json /home/eddiechang091/mission_config/
CMD ["/home/eddiechang091/entry_point/run_executable.sh"]
