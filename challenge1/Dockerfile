FROM ubuntu:focal
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install vim python3-dev python3-pip -y
RUN useradd -ms /bin/bash eddiechang091
WORKDIR /home/eddiechang091
RUN mkdir -p /home/eddiechang091/mission_config
RUN mkdir -p /home/eddiechang091/entry_point
RUN mkdir -p /home/eddiechang091/input_queue
RUN mkdir -p /home/eddiechang091/output_queue
ADD run_executable.sh /home/eddiechang091/entry_point
RUN chmod +x /home/eddiechang091/entry_point/run_executable.sh
ADD executable.py /home/eddiechang091/entry_point
ADD mission_config1714441180613.json /home/eddiechang091/mission_config
WORKDIR /home/eddiechang091/entry_point
CMD ["/home/eddiechang091/entry_point/run_executable.sh"]