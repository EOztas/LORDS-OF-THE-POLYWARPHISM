import pygame
import sys
import random

# Oyun ekranının boyutları
WIDTH = 800
HEIGHT = 600

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Savaşçı türleri ve özellikleri
WARRIOR_TYPES = {
    "Muhafız": {"kaynak": 10, "can": 80, "menzil": 1, "hasar": -20, "color": RED},
    "Okçu": {"kaynak": 20, "can": 30, "menzil": 2, "hasar": -60, "color": GREEN},
    "Topçu": {"kaynak": 50, "can": 30, "menzil": 2, "hasar": -100, "color": BLUE},
    "Atlı": {"kaynak": 30, "can": 40, "menzil": 3, "hasar": -30, "color": BLACK},
    "Sağlıkçı": {"kaynak": 10, "can": 100, "menzil": 2, "hasar": 50, "color": YELLOW}
}

# Oyuncu sınıfı
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.resources = 200  # Oyuncunun başlangıç kaynak miktarı
        self.warriors = []    # Oyuncunun sahip olduğu savaşçıların listesi

class Game:
    def __init__(self, size, num_players):
        self.size = size # Oyun alanının boyutu
        self.num_players = num_players  # Oyuncu sayısı
        self.players = [] # Oyuncuların listesi
        colors = [RED, BLUE, GREEN, YELLOW]  # Kullanılacak renklerin listesi
        for i in range(num_players):
            name = input(f"Oyuncu {i + 1} ismini girin: ") # Oyuncunun ismi kullanıcıdan alınır
            self.players.append(Player(name, colors[i]))  # Oyuncu listesine eklenir
        self.grid = [[None for _ in range(size)] for _ in range(size)] # Oyun alanını temsil eder
        self.turn = 0 # Hangi oyuncunun sırası olduğunu gösteren değişken

    def next_turn(self): #Bir sonraki turu başlatır ve her oyuncuya 10 sabit kaynak ekler

        for player in self.players:
            player.resources += 10

        self.turn = (self.turn + 1) % self.num_players # Sıra, bir sonraki oyuncuya geçirilir

    def place_warrior(self, x, y, warrior_type):
        player = self.players[self.turn] # Oyunun şu anki turundaki oyuncuyu belirler
        if warrior_type != "" and self.grid[y][x] is None: # Eğer belirtilen savaşçı türü geçerli ve belirtilen konum boş ise devam eder
            warrior_cost = WARRIOR_TYPES[warrior_type]["kaynak"] # Savaşçının kaynağı alınır
            if player.resources >= warrior_cost: # Oyuncunun kaynakları, savaşçının fiyatından fazla veya eşitse devam eder
                warrior_symbol = warrior_type + str(self.turn + 1)  # Savaşçıyı temsil eden sembolü oluşturur
                self.grid[y][x] = warrior_symbol # Savaşçıyı belirtilen konuma yerleştir
                player.resources -= warrior_cost # Oyuncunun kaynaklarını düzenler
            else:
                print("Kaynak yetersiz. Oyunu bitiriliyor.") # Eğer oyuncunun kaynakları yetersizse uyarı verilir ve oyun sonlanır
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return
        else: # Eğer belirtilen konum veya savaşçı türü geçersizse uyarı verilir
            print("Hatalı konum veya savaşçı türü. Lütfen tekrar deneyin.")
            return



    def check_winner(self):
        for player in self.players:
            warrior_count = sum( # Oyuncunun sahip olduğu savaşçıların toplam sayısını hesaplar
                row.count(player) for row in self.grid)
            if warrior_count >= (self.size ** 2) * 0.6: # Eğer oyuncunun sahip olduğu savaşçı sayısı toplam oyun alanının %60'ından fazla ise
                return player # Oyuncuyu kazanan olarak dönülür
        return None

    def ai_place_warrior(self):
        player = self.players[self.turn]
        empty_cells = [(x, y) for y in range(self.size) for x in range(self.size) if self.grid[y][x] is None] # Boş hücreler listelenir
        if empty_cells and player.resources > 0: # Boş hücreler varsa ve oyuncunun kaynakları varsa devam eder
            x, y = random.choice(empty_cells) # Rastgele bir boş hücre seçer
            warrior_type = random.choice(list(WARRIOR_TYPES.keys())) # Rastgele bir savaşçı türü seçer
            self.place_warrior(x, y, warrior_type)  # Seçilen savaşçıyı belirtilen konuma yerleştirir
            self.next_turn()

def handle_mouse_click(game, event):
    if event.button == 1: # Eğer sol fare tuşuna basıldıysa devam eder
        x, y = pygame.mouse.get_pos() # Fare konumu alınır
        # Hücre koordinatlarını hesaplar
        cell_x = x // (WIDTH // game.size)
        cell_y = y // (HEIGHT // game.size)
        player = game.players[game.turn]
        if player.name == "AI": # Eğer şu anki oyuncu yapay zeka değilse devam eder
            return
        print("Savaşçı türünü seçin:")
        print_warrior_types()
        warrior_choice = get_input("Seçiminizi yapın: ", 1, len(WARRIOR_TYPES)) # Kullanıcının savaşçı seçimi alınır
        warrior_type = list(WARRIOR_TYPES.keys())[warrior_choice - 1]
        game.place_warrior(cell_x, cell_y, warrior_type) # Savaşçıyı belirtilen konuma yerleştirir
        game.next_turn() # Bir sonraki tur başlar
        winner = game.check_winner()
        # Eğer bir kazanan varsa ekrana yazdırılır ve oyunu sonlandırılır
        if winner:
            print(f"Oyunu kazanan oyuncu: {winner.name}")
            pygame.event.post(pygame.event.Event(pygame.QUIT))

def handle_key_press(game, event):
    if event.key == pygame.K_SPACE: # Eğer basılan tuş "SPACE" ise devam eder
        game.next_turn()
        winner = game.check_winner()
        # Eğer bir kazanan varsa ekrana yazdırılır ve oyunu sonlandırılır
        if winner:
            print(f"Oyunu kazanan oyuncu: {winner.name}")
            pygame.event.post(pygame.event.Event(pygame.QUIT))

def main():
    pygame.init() # Pygame başlatılır
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Oyun ekranı oluşturulur
    pygame.display.set_caption("LORDS OF THE POLYWARPHISM") # Başlık ayarlanır
    clock = pygame.time.Clock()

    # Oyun boyutu ve oyuncu sayısı kullanıcıdan alınır
    size = get_input("Oyun boyutunu seçin (8,16 veya 32 değerini girin): ", 8, 32)
    num_players = get_input("Oyuncu sayısını belirleyin (1 ile 4 arası bir değer girin): ", 1, 4)

    game = Game(size, num_players) # Oyun nesnesi oluşturulur

    # Oyun döngüsü başlatılır
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Oyun döngüsü durdurulur
            elif event.type == pygame.MOUSEBUTTONDOWN: # Eğer fare tıklaması yapıldıysa fare işleme fonksiyonu çağırılır
                handle_mouse_click(game, event)
            elif event.type == pygame.KEYDOWN: # Eğer klavye tuşuna basıldıysa klavye işleme fonksiyonu çağırılır
                handle_key_press(game, event)

        screen.fill(WHITE) # Ekran beyaz renkle doldurulur
        draw_grid(screen, game.size) # Oyun ızgarası çizilir
        draw_warriors(screen, game.grid, game.size, game.players)  # Savaşçılar çizilir
        draw_interface(screen, game.players[game.turn]) # Arayüz çizilir
        pygame.display.flip() # Ekran güncellenir
        clock.tick(60)

        if game.players[game.turn].name == "AI": # Eğer şu anki oyuncu yapay zeka ise yapay zekanın hamlesi yapılır
            game.ai_place_warrior()

    pygame.quit() # Pygame kapatılır


# Savaşçı türlerini ekrana yazdıran fonksiyon
def print_warrior_types():
    for i, warrior_type in enumerate(WARRIOR_TYPES.keys(), start=1):
        print(f"{i}: {warrior_type}")

def draw_grid(screen, size): # Oyun alanının ızgarası çizilir
    cell_width = WIDTH // size
    cell_height = HEIGHT // size
    # Dikey çizgiler çizilir
    for x in range(0, WIDTH, cell_width):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    # Yatay çizgiler çizilir
    for y in range(0, HEIGHT, cell_height):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_warriors(screen, grid, size, players):
    cell_width = WIDTH // size
    cell_height = HEIGHT // size
    # Oyun alanındaki her hücreyi kontrol eder
    for y in range(size):
        for x in range(size):
            warrior_symbol = grid[y][x]
            # Eğer hücre boş değilse Savaşçı türü ve oyuncunun rengi alınır
            if warrior_symbol is not None:
                warrior_type = warrior_symbol[:-1]
                player_index = int(warrior_symbol[-1]) - 1  # Oyuncunun indeksi alınır
                color = players[player_index].color
                # Savaşçının görselini oluşturur ve ekrana çizer
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                pygame.draw.rect(screen, color, rect)
                font = pygame.font.Font(None, 20)
                text = font.render(warrior_symbol, True, BLACK)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                # Boş hücreler için "." karakteri gösterilir
                font = pygame.font.Font(None, 20)
                text = font.render(".", True, BLACK)
                rect = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
def draw_interface(screen, player): # Oyuncunun arayüzünü çizer
    font = pygame.font.Font(None, 36)
    text = font.render(f"{player.name} - Kaynak: {player.resources}", True, player.color)  # Oyuncunun adı ve kaynak miktarını ekrana yazdırır
    screen.blit(text, (10, 10))


def get_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt)) # Kullanıcıdan bir değer istenir
            if min_value <= value <= max_value: # Girilen değer aralık kontrolü yapılır
                return value
            else:
                print("Lütfen 8,16 veya 32 değerini girin.") # Aralık dışındaki girişler için uyarı verilir
        except ValueError:
            print("Geçersiz giriş, lütfen bir sayı girin.") # Sayısal olmayan girişler için hata mesajı verilir

if __name__ == "__main__":
    try:
        main()  # Ana program başlatılır
    except KeyboardInterrupt:
        print("Oyun kapatıldı.") # Oyun kapatılınca bilgilendirme mesajı ekranda gösterilir.
        pygame.quit() # Pygame kapatılır
        sys.exit() # Programdan çıkılır

