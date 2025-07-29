#!/bin/bash
rclone sync gdrive:paper_tasks ./gdrive_inbox --create-empty-src-dirs
