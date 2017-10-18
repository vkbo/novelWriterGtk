# -*- coding: utf-8 -*
"""novelWriter Content Functions

 novelWriter – Content Functions
=================================
 A collection of functions that return text and html

 File History:
 Created:   2017-10-05 [0.4.0]

"""

import logging
import nw

logger = logging.getLogger(__name__)

def getLoremIpsum(nPar):
    """
    Returns up to 13 paragraphs of Lorem Ipsum.
    Text from http://www.lipsum.com
    """
    
    if nPar > 13:
        logger.debug("Requested more than 13 elements from getLoremIpsum")
        nPar = 13
    
    pArray = [(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vulputate luctus quam, in "
        "congue elit viverra malesuada. Ut iaculis quam fringilla ex aliquam auctor. Nam eu libero "
        "ac arcu egestas malesuada ut vel nisi. Maecenas et mauris dignissim, ultricies neque et, o"
        "rnare diam. In vitae libero consequat, consequat eros nec, rhoncus velit. Class aptent tac"
        "iti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Etiam et eleme"
        "ntum quam. Suspendisse laoreet dapibus vulputate. Phasellus turpis purus, convallis quis b"
        "ibendum non, tincidunt eu libero. Fusce finibus sem velit, vitae dapibus ante tincidunt ac"
        ". Morbi in consequat turpis. Suspendisse felis dui, tincidunt sit amet lacinia eget, viver"
        "ra ut arcu. Vivamus auctor nunc nunc, vitae porta sem tempus sed."),("Cras orci leo, digni"
        "ssim quis turpis quis, sodales faucibus diam. Nam dictum dignissim lorem eget condimentum."
        " Sed consequat elit ut purus convallis, sit amet blandit tellus convallis. Phasellus sit a"
        "met scelerisque mauris, id euismod risus. Interdum et malesuada fames ac ante ipsum primis"
        " in faucibus. Nunc ornare, felis in varius pulvinar, diam erat vehicula quam, posuere mole"
        "stie erat turpis in neque. Sed ornare, justo a consectetur aliquet, lorem lorem posuere pu"
        "rus, nec tristique dolor ipsum sed nisi."),("Sed at congue nisi, non consequat est. Mauris"
        " nec lacinia purus, sed ullamcorper sapien. Morbi faucibus facilisis ullamcorper. Praesent"
        " sodales vulputate eros, et sagittis eros viverra quis. In hac habitasse platea dictumst. "
        "Nullam eleifend, est dignissim varius lacinia, augue nunc fermentum orci, in suscipit nequ"
        "e nisi in augue. Praesent pharetra posuere sollicitudin. Phasellus ac dapibus sapien. Maur"
        "is fringilla metus ac justo maximus, id venenatis lorem imperdiet. Morbi tincidunt turpis "
        "ac mauris facilisis, et facilisis lacus finibus. Donec gravida felis lacus, et aliquam lor"
        "em convallis vel. Integer rhoncus placerat lectus eu pharetra. Mauris mi diam, ultrices in"
        " fermentum sed, feugiat ut augue. Fusce sollicitudin varius enim, id pretium nunc placerat"
        " nec. Aenean eget neque dapibus, blandit magna vel, placerat tellus. Etiam et porta sapien"
        "."),("Nullam rhoncus commodo leo, vitae imperdiet nunc suscipit sed. Suspendisse iaculis c"
        "ongue dolor, in congue urna tincidunt sit amet. Nam facilisis, arcu et ultricies blandit, "
        "ante quam mollis magna, eu cursus ipsum nisi et turpis. Nullam quis sem at ligula posuere "
        "pretium. Etiam justo neque, efficitur et vulputate sit amet, pharetra eget orci. Sed moles"
        "tie congue ante sit amet pulvinar. Nullam commodo turpis sed rhoncus facilisis. Quisque ve"
        "l sagittis lacus. Fusce nulla sem, tincidunt ac tempus at, ultrices consequat nisl. Donec "
        "interdum ante urna, eu scelerisque mauris efficitur et. Quisque nec faucibus metus. Sed ve"
        "stibulum urna quis odio pulvinar pretium. Integer ullamcorper dictum tincidunt."),("Intege"
        "r rutrum felis augue, sed fringilla tortor molestie eget. Suspendisse sit amet efficitur r"
        "isus. In odio ex, congue quis lectus fermentum, blandit venenatis lorem. Sed ut arcu erat."
        " Pellentesque vitae elit ornare, aliquam lacus sit amet, molestie mauris. Donec eget luctu"
        "s lectus, in dignissim orci. Aenean id pretium ligula. Etiam pulvinar sagittis pharetra. F"
        "usce eu tortor vitae ligula laoreet gravida ut vitae leo. Morbi non elementum est, eu plac"
        "erat lorem. In hac habitasse platea dictumst. Aliquam erat volutpat. Aenean at quam laoree"
        "t, ullamcorper dui et, lacinia est. Vivamus vitae lectus sed elit mollis semper nec ut dia"
        "m. Etiam ex tortor, interdum quis urna viverra, auctor ornare leo."),("Praesent ultricies "
        "sollicitudin tincidunt. Praesent porta, risus quis consequat dapibus, ipsum arcu sollicitu"
        "din nulla, a elementum ipsum libero nec libero. Proin viverra turpis id erat auctor sollic"
        "itudin. In et tincidunt nulla. Vestibulum faucibus laoreet molestie. Aenean sed dignissim "
        "diam. Pellentesque sed justo malesuada tellus pretium dignissim a sed ante. Nunc dictum bl"
        "andit vulputate. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per i"
        "nceptos himenaeos. Sed at eleifend orci. Aliquam mattis, erat vitae aliquam volutpat, arcu"
        " augue pharetra diam, tempor ultricies arcu ante a ligula."),("Proin sit amet orci at diam"
        " porta porta. Sed orci nibh, interdum nec viverra quis, bibendum vitae odio. Nam auctor ve"
        "hicula tellus, at iaculis arcu ornare et. Phasellus dolor nisl, ultricies vitae justo id, "
        "vehicula laoreet odio. In imperdiet nisi at dapibus suscipit. Sed vel justo non erat rutru"
        "m volutpat at eu ante. Integer scelerisque varius nunc, sit amet sollicitudin magna ultric"
        "es a."),("Nam ac mauris ante. Cras imperdiet neque a orci vulputate, at laoreet ante aucto"
        "r. Donec sit amet lobortis leo. Donec ac mauris in orci commodo venenatis ut sed magna. Nu"
        "nc vehicula in lacus eget feugiat. Nulla vel sagittis nulla, non tincidunt lectus. Nunc ac"
        " arcu a nisl interdum dapibus sed at urna. Nulla aliquam sollicitudin quam, vel dignissim "
        "elit feugiat at. Donec bibendum nunc libero. Suspendisse potenti."),("Nunc ac dignissim ip"
        "sum. Curabitur dictum non arcu et ornare. Curabitur lacinia, felis id ullamcorper tincidun"
        "t, est lorem consectetur risus, non ornare turpis risus ut arcu. Nullam et consequat eros."
        " In ornare eget elit vitae maximus. Cras sodales sem non massa pharetra semper. Nulla vive"
        "rra, leo et sagittis varius, diam est consectetur diam, quis auctor neque lectus vitae odi"
        "o. Nullam at interdum ipsum. Nullam volutpat metus in dolor rhoncus, sit amet ornare erat "
        "condimentum. Quisque eros libero, auctor ac aliquet nec, ornare quis nulla. Nunc euismod j"
        "usto in purus fermentum placerat. Sed hendrerit neque eros, quis finibus lacus blandit ac."
        " Ut placerat, augue eu facilisis pretium, nulla nisl euismod massa, a ultricies odio neque"
        " nec urna. Phasellus ac vehicula elit. Cras odio lectus, dapibus at interdum quis, condime"
        "ntum a arcu. Maecenas rhoncus augue ac accumsan sagittis."),("Integer eu ex massa. Quisque"
        " lacinia nisi vitae nunc faucibus rhoncus. Nunc magna odio, porttitor quis lacus vitae, co"
        "ngue fringilla enim. Mauris quis placerat magna. Nullam faucibus justo quis facilisis tris"
        "tique. Praesent sollicitudin nulla quis mi tincidunt pellentesque. Nulla nibh enim, lobort"
        "is in lectus ac, condimentum aliquam mauris. Nunc ut sapien commodo, varius quam ac, posue"
        "re ex. Vestibulum tempor augue id ex convallis consectetur."),("Cras bibendum eleifend fac"
        "ilisis. Mauris viverra, eros pulvinar euismod consequat, ipsum arcu dignissim lectus, a ia"
        "culis enim arcu vel nunc. Mauris fermentum ac turpis pretium blandit. Integer fringilla pl"
        "acerat placerat. Nam leo ex, venenatis at nisl ac, vestibulum luctus est. Donec porta matt"
        "is ipsum, et faucibus ex sagittis et. Mauris rhoncus leo id ante semper sollicitudin."),(""
        "Cras sit amet molestie purus. Suspendisse dolor felis, molestie in mi vel, feugiat cursus "
        "elit. Donec non nunc quis justo bibendum rhoncus vitae tincidunt felis. Donec dapibus soll"
        "icitudin nisi, sit amet consectetur lectus rutrum sit amet. Sed auctor erat arcu, vel fini"
        "bus massa dapibus id. Quisque laoreet venenatis ornare. Nam id enim nisi. Quisque sceleris"
        "que ut dui sed tempus. Sed augue risus, eleifend eget ipsum id, rhoncus fermentum velit. N"
        "ulla viverra ex sed erat iaculis, ut ullamcorper enim finibus."),("Praesent finibus erat n"
        "ec tempor feugiat. Duis sit amet condimentum nunc, consequat aliquam elit. Pellentesque li"
        "gula elit, tempus in ipsum molestie, gravida consequat orci. Maecenas eget mauris urna. Nu"
        "nc sodales ante vel vulputate luctus. Nunc a erat dolor. Etiam at tellus nec velit consequ"
        "at dapibus"
    )]
    
    return pArray[0:nPar]
