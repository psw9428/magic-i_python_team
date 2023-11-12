plane_info =[]
def print_plain() :
    plane_array = []
    size = 41
    half = size//2
    for i in range(0, size) :
        a = []
        for j in range(0, size) :
            a.append('X')
        plane_array.append(a)
    i = -half
    while i <= half :
        j = -half
        while j <= half :
            tmp = infos.publicPlane[i, j]
            #plane_array[i + half][j + half] = tmp.r_toOccupy
            if tmp.r_toOccupy == 0 :
                plane_array[i+half][j+half] = 'O'
            if (tmp.r_toBuildBase > 0 and int(25 * 1.6 ** ((abs(i) + abs(j))/512)) > tmp.r_toBuildBase) :
                plane_array[i+half][j+half] = 'N'
            if (tmp.r_toBuildBase == 0) :
                plane_array[i+half][j+half] = 'B'
            if (tmp.r_toBuildTeleporter == 0) :
                plane_array[i+half][j+half] = 'T'
            if (tmp.count_characters > 0) :
                plane_array[i+half][j+half] = 'P'
            j += 1
        i += 1
    plane_array[infos.pos_me[0] + half][infos.pos_me[1] + half] = '@'
    return plane_array