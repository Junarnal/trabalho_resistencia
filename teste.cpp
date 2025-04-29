#include <SFML/Graphics.hpp>

int main() {
    sf::RenderWindow window(sf::VideoMode(800, 600), "Plano Cartesiano com Mouse");
    window.setFramerateLimit(60);

    // Centro inicial do plano
    sf::Vector2f center(400, 300);

    // Variáveis para arrastar com o mouse
    bool dragging = false;
    sf::Vector2f previousMousePos;

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed)
                window.close();

            // Detectar início do clique
            if (event.type == sf::Event::MouseButtonPressed) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    dragging = true;
                    previousMousePos = window.mapPixelToCoords(sf::Mouse::getPosition(window));
                }
            }

            // Detectar fim do clique
            if (event.type == sf::Event::MouseButtonReleased) {
                if (event.mouseButton.button == sf::Mouse::Left) {
                    dragging = false;
                }
            }

            // Detectar movimento do mouse enquanto arrasta
            if (event.type == sf::Event::MouseMoved) {
                if (dragging) {
                    sf::Vector2f currentMousePos = window.mapPixelToCoords(sf::Mouse::getPosition(window));
                    sf::Vector2f delta = currentMousePos - previousMousePos;
                    center += delta;
                    previousMousePos = currentMousePos;
                }
            }
        }

        window.clear(sf::Color::White);

        // Desenhar o eixo X
        sf::Vertex xAxis[] =
        {
            sf::Vertex(sf::Vector2f(0, center.y), sf::Color::Black),
            sf::Vertex(sf::Vector2f(window.getSize().x, center.y), sf::Color::Black)
        };

        // Desenhar o eixo Y
        sf::Vertex yAxis[] =
        {
            sf::Vertex(sf::Vector2f(center.x, 0), sf::Color::Black),
            sf::Vertex(sf::Vector2f(center.x, window.getSize().y), sf::Color::Black)
        };

        window.draw(xAxis, 2, sf::Lines);
        window.draw(yAxis, 2, sf::Lines);

        // Desenhar marcações no eixo
        for (int i = -1000; i <= 1000; i += 50) {
            // Marcações no eixo X
            sf::Vertex markX[] =
            {
                sf::Vertex(sf::Vector2f(center.x + i, center.y - 5), sf::Color::Black),
                sf::Vertex(sf::Vector2f(center.x + i, center.y + 5), sf::Color::Black)
            };
            window.draw(markX, 2, sf::Lines);

            // Marcações no eixo Y
            sf::Vertex markY[] =
            {
                sf::Vertex(sf::Vector2f(center.x - 5, center.y + i), sf::Color::Black),
                sf::Vertex(sf::Vector2f(center.x + 5, center.y + i), sf::Color::Black)
            };
            window.draw(markY, 2, sf::Lines);
        }

        window.display();
    }

    return 0;
}

