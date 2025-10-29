# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: ndahib <ndahib@student.1337.ma>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/10/29 14:11:04 by ndahib            #+#    #+#              #
#    Updated: 2025/10/29 14:11:04 by ndahib           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from core.management import Management
import sys


def main():
    manager = Management(sys.argv[1:])
    manager.execute()


if __name__ == "__main__":
    main()
